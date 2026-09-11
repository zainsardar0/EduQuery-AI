SET NOCOUNT ON;
SET XACT_ABORT ON;

IF OBJECT_ID(N'eduquery_reporting.HOF_FRMT_SOURCE_V1', N'V') IS NULL
    THROW 51000, 'Run 002_reporting_views.sql first.', 1;

IF OBJECT_ID(N'eduquery_reporting.HOF_FRMT_CACHE_V1', N'U') IS NULL
BEGIN
    CREATE TABLE eduquery_reporting.HOF_FRMT_CACHE_V1 (
        CacheRowId bigint IDENTITY(1,1) NOT NULL CONSTRAINT PK_HOF_FRMT_CACHE_V1 PRIMARY KEY,
        EID float NULL, NAME nvarchar(400) NULL, SUBJECT nvarchar(400) NULL, SCHOOL nvarchar(200) NULL,
        [Year] float NULL, [CLASS/SECTION] nvarchar(32) NULL, APPEARED int NULL,
        [PASS%] decimal(9,2) NULL, [PASS% OF BOARD] decimal(9,2) NULL, Position int NULL,
        TOTAL_POSITIONS int NULL, [WORK LOAD] int NULL, [CLASS AVG] float NULL,
        [ABOVE 90%] int NULL, [ABOVE 80%] int NULL, [ABOVE 70%] int NULL,
        [ABOVE 60%] int NULL, [ABOVE 50%] int NULL, [ABOVE 40%] int NULL,
        [BELOW 40%] int NULL, [ABOVE 70 %] decimal(9,2) NULL, [ABOVE 70 COUNT] int NULL,
        [BELOW 70 %] decimal(9,2) NULL, [BELOW 70% COUNT] int NULL, REMARKS varchar(1) NOT NULL
    );
    CREATE INDEX IX_HOF_FRMT_CACHE_V1_Filter
        ON eduquery_reporting.HOF_FRMT_CACHE_V1 (SCHOOL, [Year], SUBJECT, EID);
END;

IF OBJECT_ID(N'eduquery_reporting.INTERNAL_EXAM_GROUP_CACHE_V1', N'U') IS NULL
BEGIN
    CREATE TABLE eduquery_reporting.INTERNAL_EXAM_GROUP_CACHE_V1 (
        CacheRowId bigint IDENTITY(1,1) NOT NULL CONSTRAINT PK_INTERNAL_EXAM_GROUP_CACHE_V1 PRIMARY KEY,
        ID int NOT NULL, SCHOOL varchar(10) NOT NULL, EXAMTYPE nvarchar(50) NOT NULL,
        EID int NOT NULL, [TEACHER NAME] nvarchar(100) NOT NULL, [YEAR] int NOT NULL,
        CLASS int NOT NULL, SECTION char(1) NOT NULL, SUBJECT nvarchar(50) NOT NULL,
        [GROUP] varchar(50) NULL, APPEARED int NULL, ABSENT int NULL, [PASS] int NULL,
        [A+] int NULL, A int NULL, B int NULL, C int NULL, D int NULL, E int NULL, F int NULL,
        [CLASS%] decimal(10,2) NULL, CLASS_AVG decimal(10,2) NULL,
        [BELOW 70%] int NULL, [ABOVE 70%] int NULL
    );
    CREATE INDEX IX_INTERNAL_EXAM_GROUP_CACHE_V1_Filter
        ON eduquery_reporting.INTERNAL_EXAM_GROUP_CACHE_V1
        (SCHOOL, [YEAR], EXAMTYPE, CLASS, SECTION, SUBJECT) INCLUDE (EID, [GROUP], [CLASS%], CLASS_AVG);
END;

EXEC(N'
CREATE OR ALTER PROCEDURE eduquery_reporting.RefreshPerformanceCaches
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    DECLARE @StartedAt datetime2(0) = SYSUTCDATETIME();
    DECLARE @LockResult int;
    EXEC @LockResult = sys.sp_getapplock
        @Resource = N''eduquery_reporting.RefreshPerformanceCaches'',
        @LockMode = N''Exclusive'', @LockOwner = N''Session'', @LockTimeout = 0;
    IF @LockResult < 0 THROW 51010, ''A reporting refresh is already running.'', 1;

    BEGIN TRY
        BEGIN TRANSACTION;
        TRUNCATE TABLE eduquery_reporting.HOF_FRMT_CACHE_V1;
        INSERT eduquery_reporting.HOF_FRMT_CACHE_V1
            (EID, NAME, SUBJECT, SCHOOL, [Year], [CLASS/SECTION], APPEARED, [PASS%], [PASS% OF BOARD],
             Position, TOTAL_POSITIONS, [WORK LOAD], [CLASS AVG], [ABOVE 90%], [ABOVE 80%],
             [ABOVE 70%], [ABOVE 60%], [ABOVE 50%], [ABOVE 40%], [BELOW 40%], [ABOVE 70 %],
             [ABOVE 70 COUNT], [BELOW 70 %], [BELOW 70% COUNT], REMARKS)
        SELECT EID, NAME, SUBJECT, SCHOOL, [Year], [CLASS/SECTION], APPEARED, [PASS%], [PASS% OF BOARD],
               Position, TOTAL_POSITIONS, [WORK LOAD], [CLASS AVG], [ABOVE 90%], [ABOVE 80%],
               [ABOVE 70%], [ABOVE 60%], [ABOVE 50%], [ABOVE 40%], [BELOW 40%], [ABOVE 70 %],
               [ABOVE 70 COUNT], [BELOW 70 %], [BELOW 70% COUNT], REMARKS
        FROM eduquery_reporting.HOF_FRMT_SOURCE_V1;

        TRUNCATE TABLE eduquery_reporting.INTERNAL_EXAM_GROUP_CACHE_V1;
        INSERT eduquery_reporting.INTERNAL_EXAM_GROUP_CACHE_V1
            (ID, SCHOOL, EXAMTYPE, EID, [TEACHER NAME], [YEAR], CLASS, SECTION, SUBJECT, [GROUP],
             APPEARED, ABSENT, [PASS], [A+], A, B, C, D, E, F, [CLASS%], CLASS_AVG, [BELOW 70%], [ABOVE 70%])
        SELECT ID, SCHOOL, EXAMTYPE, EID, [TEACHER NAME], [YEAR], CLASS, SECTION, SUBJECT, [GROUP],
               APPEARED, ABSENT, [PASS], [A+], A, B, C, D, E, F, [CLASS%], CLASS_AVG, [BELOW 70%], [ABOVE 70%]
        FROM dbo.INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW;

        IF NOT EXISTS (SELECT 1 FROM eduquery_reporting.HOF_FRMT_CACHE_V1)
            THROW 51011, ''HOF materialization produced no rows.'', 1;
        IF NOT EXISTS (SELECT 1 FROM eduquery_reporting.INTERNAL_EXAM_GROUP_CACHE_V1)
            THROW 51012, ''Internal materialization produced no rows.'', 1;

        MERGE eduquery_reporting.MaterializationState AS target
        USING (VALUES
            (N''HOF_FRMT'', CONVERT(bigint, (SELECT COUNT_BIG(*) FROM eduquery_reporting.HOF_FRMT_CACHE_V1))),
            (N''INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW'', CONVERT(bigint, (SELECT COUNT_BIG(*) FROM eduquery_reporting.INTERNAL_EXAM_GROUP_CACHE_V1)))
        ) AS source (ObjectName, [RowCount])
        ON target.ObjectName = source.ObjectName
        WHEN MATCHED THEN UPDATE SET LastStartedAt = @StartedAt, LastSucceededAt = SYSUTCDATETIME(),
             [RowCount] = source.[RowCount], DurationMs = DATEDIFF(millisecond, @StartedAt, SYSUTCDATETIME()), LastErrorCode = NULL
        WHEN NOT MATCHED THEN INSERT (ObjectName, LastStartedAt, LastSucceededAt, [RowCount], DurationMs)
             VALUES (source.ObjectName, @StartedAt, SYSUTCDATETIME(), source.[RowCount],
                     DATEDIFF(millisecond, @StartedAt, SYSUTCDATETIME()));
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;
');

EXEC(N'CREATE OR ALTER VIEW eduquery_reporting.HOF_FRMT AS
      SELECT EID, NAME, SUBJECT, SCHOOL, [Year], [CLASS/SECTION], APPEARED, [PASS%], [PASS% OF BOARD],
             Position, TOTAL_POSITIONS, [WORK LOAD], [CLASS AVG], [ABOVE 90%], [ABOVE 80%],
             [ABOVE 70%], [ABOVE 60%], [ABOVE 50%], [ABOVE 40%], [BELOW 40%], [ABOVE 70 %],
             [ABOVE 70 COUNT], [BELOW 70 %], [BELOW 70% COUNT], REMARKS
      FROM eduquery_reporting.HOF_FRMT_CACHE_V1;');

EXEC(N'CREATE OR ALTER VIEW eduquery_reporting.INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW AS
      SELECT ID, SCHOOL, EXAMTYPE, EID, [TEACHER NAME], [YEAR], CLASS, SECTION, SUBJECT, [GROUP],
             APPEARED, ABSENT, [PASS], [A+], A, B, C, D, E, F, [CLASS%], CLASS_AVG, [BELOW 70%], [ABOVE 70%]
      FROM eduquery_reporting.INTERNAL_EXAM_GROUP_CACHE_V1;');

EXEC eduquery_reporting.RefreshPerformanceCaches;
