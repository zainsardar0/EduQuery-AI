SET NOCOUNT ON;
SET XACT_ABORT ON;

DECLARE @ContractVersion varchar(32) = '2026.08.16.1';

IF EXISTS (
    SELECT 1
    FROM eduquery_reporting.PassThresholdRule AS a
    JOIN eduquery_reporting.PassThresholdRule AS b
      ON a.RuleId < b.RuleId AND a.IsActive = 1 AND b.IsActive = 1
     AND a.ClassFrom <= b.ClassTo AND b.ClassFrom <= a.ClassTo
     AND a.YearFrom <= b.YearTo AND b.YearFrom <= a.YearTo
)
    THROW 51030, 'Active pass-threshold rules overlap.', 1;

IF EXISTS (
    SELECT 1
    FROM (SELECT DISTINCT TRY_CONVERT(int, CLASS) AS ClassLevel, YEAR
          FROM dbo.STUDENTS_ROLL_INTERNAL_EXAM) AS live_grain
    WHERE live_grain.ClassLevel IS NOT NULL
      AND NOT EXISTS (
          SELECT 1 FROM eduquery_reporting.PassThresholdRule AS threshold_rule
          WHERE threshold_rule.IsActive = 1
            AND live_grain.ClassLevel BETWEEN threshold_rule.ClassFrom AND threshold_rule.ClassTo
            AND live_grain.YEAR BETWEEN threshold_rule.YearFrom AND threshold_rule.YearTo
      )
)
    THROW 51031, 'A live class/year combination has no approved pass-threshold rule.', 1;

IF EXISTS (SELECT 1 FROM eduquery_reporting.INTERNAL_STUDENT_GRAIN_CONFLICTS_V1)
    THROW 51032, 'Conflicting internal student grains must be resolved before activation.', 1;

IF OBJECT_ID(N'eduquery_reporting.STUDENT_SUBJECT_POSITION_V1', N'V') IS NULL
    THROW 51033, 'The certified student subject-position view is missing.', 1;

IF EXISTS (
    SELECT 1
    FROM dbo.EDUQUERY_STUDENT_SUBJECT_RESULT_SOURCE
    WHERE UPPER(LTRIM(RTRIM(SUBJECT))) <> 'TOTAL'
    GROUP BY CAMPUS, SCHOOL_YEAR, CLASS_LEVEL, STUDENT_REFERENCE, UPPER(LTRIM(RTRIM(SUBJECT)))
    HAVING COUNT_BIG(*) <> 1
)
    THROW 51034, 'The certified student subject source violates its unique grain.', 1;

IF EXISTS (
    SELECT required.ObjectName
    FROM (VALUES (N'HOF_FRMT'), (N'INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW')) AS required(ObjectName)
    LEFT JOIN eduquery_reporting.MaterializationState AS state ON state.ObjectName = required.ObjectName
    WHERE state.LastSucceededAt IS NULL OR state.LastSucceededAt < DATEADD(hour, -24, SYSUTCDATETIME())
       OR ISNULL(state.[RowCount], 0) = 0
)
    THROW 51035, 'A required materialization is missing, stale, or empty.', 1;

BEGIN TRANSACTION;
UPDATE eduquery_reporting.SemanticContract SET IsActive = 0 WHERE IsActive = 1;
UPDATE eduquery_reporting.SemanticContract
SET IsActive = 1, ActivatedAt = SYSUTCDATETIME(), AppliedBy = ORIGINAL_LOGIN()
WHERE ContractVersion = @ContractVersion;
IF @@ROWCOUNT <> 1
    THROW 51036, 'The semantic contract registration is missing.', 1;
COMMIT TRANSACTION;
