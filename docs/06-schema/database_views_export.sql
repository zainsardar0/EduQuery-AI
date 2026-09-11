-- ==============================================================================
-- EduQuery AI Master View Definitions Export (Verified Live Candidate)
-- Database Target: db_aadc11_sqldaanish
-- Verified Live View Count: 68
-- Export Mode: Read-Only Extraction from sys.views and sys.sql_modules
-- Deterministic Ordering: Alphabetical by schema_name, view_name
-- Generated Date: 2026-08-03
-- ==============================================================================

-- View: [dbo].[ALL_BOARD_MIDDLE] (Object ID: 750625717)
-- Created: 2025-05-27T11:40:41.443 | Modified: 2025-05-27T11:41:32.853
-- Final Summary View with Dense Ranked POSITION_TEXT using BOARD_MIDDLE view
CREATE VIEW [dbo].[ALL_BOARD_MIDDLE] AS 
WITH RankedPositions AS (
    SELECT
        EID,
        SUBJECT,
        AVG(Position) AS AvgPosition
    FROM BOARD_MIDDLE
    WHERE CATEGROY = 'BOARD'
    GROUP BY EID, SUBJECT
),
RenumberedRanks AS (
    SELECT
        EID,
        SUBJECT,
        DENSE_RANK() OVER (ORDER BY AvgPosition ASC) AS RenumberedPosition
    FROM RankedPositions
),
TotalRanks AS (
    SELECT COUNT(*) AS TotalPositions FROM RenumberedRanks
),
BaseData AS (
    SELECT 
        main.EID,
        MAX(main.NAME) AS NAME,
        MAX(main.SCHOOL) AS SCHOOL,
        NULL AS EXAMTYPE,
        main.SUBJECT,
        NULL AS CLASS,
        NULL AS SECTION,
        NULL AS Year,
        main.CATEGROY,
        MAX(main.[SCHOOL-MERGE]) AS [SCHOOL-MERGE],
        MAX(main.SUBJECT_MERGE) AS SUBJECT_MERGE,
        SUM(main.STRENGTH) AS STRENGTH,
        SUM(main.Count_90_100) AS Count_90_100,
        SUM(main.Count_80_90) AS Count_80_90,
        SUM(main.Count_70_80) AS Count_70_80,
        SUM(main.Count_60_70) AS Count_60_70,
        SUM(main.Count_50_60) AS Count_50_60,
        SUM(main.Count_40_50) AS Count_40_50,
        SUM(main.Count_0_39) AS Count_0_39,
        SUM(main.Above_70) AS Above_70,
        SUM(main.Below_70) AS Below_70,
        SUM(main.APPEARED) AS APPEARED,
        SUM(main.PASSED) AS PASSED,
        SUM(main.[CLASS AVG]) AS TotalClassAvg,
        COUNT(main.[CLASS AVG]) AS CountClassAvg,
        SUM(main.Position) AS TotalPosition,
        COUNT(main.Position) AS CountPosition,
        SUM(main.TOTAL_POSITIONS) AS TotalPos,
        SUM(main.WL) AS TotalWL
    FROM BOARD_MIDDLE main
    GROUP BY main.EID, main.SUBJECT, main.CATEGROY
),
BoardCareer AS (
    SELECT
        EID,
        MAX(NAME) AS NAME,
        MAX(SCHOOL) AS SCHOOL,
        NULL AS EXAMTYPE,
        NULL AS SUBJECT,
        NULL AS CLASS,
        NULL AS SECTION,
        NULL AS Year,
        'BOARD_CAREER' AS CATEGROY,
        MAX([SCHOOL-MERGE]) AS [SCHOOL-MERGE],
        MAX(SUBJECT_MERGE) AS SUBJECT_MERGE,
        SUM(STRENGTH) AS STRENGTH,
        CAST(SUM(Count_90_100) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Count_90_100,
        CAST(SUM(Count_80_90) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Count_80_90,
        CAST(SUM(Count_70_80) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Count_70_80,
        CAST(SUM(Count_60_70) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Count_60_70,
        CAST(SUM(Count_50_60) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Count_50_60,
        CAST(SUM(Count_40_50) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Count_40_50,
        CAST(SUM(Count_0_39) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Count_0_39,
        CAST(SUM(Above_70) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Above_70,
        CAST(SUM(Below_70) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Below_70,
        SUM(APPEARED) AS APPEARED,
        SUM(PASSED) AS PASSED,
        CAST(SUM(PASSED) * 100.0 / NULLIF(SUM(APPEARED),0) AS DECIMAL(5,2)) AS [PASS%],
        CAST(SUM(TotalClassAvg) / NULLIF(SUM(CountClassAvg),0) AS DECIMAL(5,2)) AS [CLASS AVG],
        FLOOR(SUM(TotalPosition) * 1.0 / NULLIF(SUM(CountPosition),0)) AS Position,
        FLOOR(SUM(TotalPos) * 1.0 / NULLIF(SUM(CountPosition),0)) AS TOTAL_POSITIONS,
        FLOOR(SUM(TotalWL) * 1.0 / NULLIF(SUM(CountPosition),0)) AS WL
    FROM BaseData
    WHERE CATEGROY = 'BOARD'
    GROUP BY EID
),
MiddleCareer AS (
    SELECT
        EID,
        MAX(NAME) AS NAME,
        MAX(SCHOOL) AS SCHOOL,
        NULL AS EXAMTYPE,
        NULL AS SUBJECT,
        NULL AS CLASS,
        NULL AS SECTION,
        NULL AS Year,
        'MIDDLE_CAREER' AS CATEGROY,
        MAX([SCHOOL-MERGE]) AS [SCHOOL-MERGE],
        MAX(SUBJECT_MERGE) AS SUBJECT_MERGE,
        SUM(STRENGTH) AS STRENGTH,
        CAST(SUM(Count_90_100) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Count_90_100,
        CAST(SUM(Count_80_90) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Count_80_90,
        CAST(SUM(Count_70_80) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Count_70_80,
        CAST(SUM(Count_60_70) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Count_60_70,
        CAST(SUM(Count_50_60) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Count_50_60,
        CAST(SUM(Count_40_50) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Count_40_50,
        CAST(SUM(Count_0_39) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Count_0_39,
        CAST(SUM(Above_70) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Above_70,
        CAST(SUM(Below_70) * 100.0 / NULLIF(SUM(STRENGTH),0) AS DECIMAL(5,2)) AS Below_70,
        SUM(APPEARED) AS APPEARED,
        SUM(PASSED) AS PASSED,
        CAST(SUM(PASSED) * 100.0 / NULLIF(SUM(APPEARED),0) AS DECIMAL(5,2)) AS [PASS%],
        CAST(SUM(TotalClassAvg) / NULLIF(SUM(CountClassAvg),0) AS DECIMAL(5,2)) AS [CLASS AVG],
        FLOOR(SUM(TotalPosition) * 1.0 / NULLIF(SUM(CountPosition),0)) AS Position,
        FLOOR(SUM(TotalPos) * 1.0 / NULLIF(SUM(CountPosition),0)) AS TOTAL_POSITIONS,
        FLOOR(SUM(TotalWL) * 1.0 / NULLIF(SUM(CountPosition),0)) AS WL
    FROM BaseData
    WHERE CATEGROY = 'MIDDLE'
    GROUP BY EID
)

-- Final Output
SELECT * FROM BoardCareer
UNION ALL
SELECT * FROM MiddleCareer;

GO

-- View: [dbo].[ALL_COMBINED2] (Object ID: 635149308)
-- Created: 2025-06-19T12:22:58.450 | Modified: 2025-06-19T12:22:58.450
CREATE VIEW [dbo].[ALL_COMBINED2] AS  
SELECT DISTINCT  
    CAST([EID] AS NVARCHAR(50)) AS [EID],  
    CAST([NAME] AS NVARCHAR(255)) AS [NAME],  
    CAST([SCHOOL] AS NVARCHAR(255)) AS [SCHOOL],  
    CASE WHEN [CATEGROY] = 'BOARD_ALL' THEN NULL ELSE CAST([SUBJECT] AS NVARCHAR(100)) END AS [SUBJECT],  
    CAST([CLASS] AS NVARCHAR(50)) AS [CLASS],  
    CAST([SECTION] AS NVARCHAR(50)) AS [SECTION],  
    CAST([Year] AS NVARCHAR(10)) AS [Year],  
    CAST([CATEGROY] AS NVARCHAR(50)) AS [CATEGROY],  
    CAST([STRENGTH] AS NVARCHAR(20)) AS [STRENGTH],  
    CAST([Count_90_100] AS NVARCHAR(20)) AS [Count_90_100],  
    CAST([Count_80_90] AS NVARCHAR(20)) AS [Count_80_90],  
    CAST([Count_70_80] AS NVARCHAR(20)) AS [Count_70_80],  
    CAST([Count_60_70] AS NVARCHAR(20)) AS [Count_60_70],  
    CAST([Count_50_60] AS NVARCHAR(20)) AS [Count_50_60],  
    CAST([Count_40_50] AS NVARCHAR(20)) AS [Count_40_50],  
    CAST([Count_0_39] AS NVARCHAR(20)) AS [Count_0_39],  
    CAST([Above_70] AS NVARCHAR(20)) AS [Above_70],  
    CAST([Below_70] AS NVARCHAR(20)) AS [Below_70],  
    CAST([APPEARED] AS NVARCHAR(20)) AS [APPEARED],  
    CAST([PASSED] AS NVARCHAR(20)) AS [PASSED],  
    CAST([PASS%] AS NVARCHAR(20)) AS [PASS%],  
    CAST([CLASS AVG] AS NVARCHAR(20)) AS [CLASS AVG],  
    CAST([Position] AS NVARCHAR(50)) AS [Position],  
    CAST([TOTAL_POSITIONS] AS NVARCHAR(20)) AS [TOTAL_POSITIONS],  
    CAST([WL] AS NVARCHAR(20)) AS [WL],  
    CAST([SCHOOL-MERGE] AS NVARCHAR(255)) AS [SCHOOL-MERGE],  
    CAST([SUBJECT_MERGE] AS NVARCHAR(255)) AS [SUBJECT_MERGE]  
FROM TR_ALL_IND_POS  

UNION  

SELECT DISTINCT  
    CAST([EID] AS NVARCHAR(50)),  
    CAST([NAME] AS NVARCHAR(255)),  
    CAST([SCHOOL] AS NVARCHAR(255)),  
    CASE WHEN [CATEGROY] = 'BOARD_ALL' THEN NULL ELSE CAST([SUBJECT] AS NVARCHAR(100)) END,  
    CAST([CLASS] AS NVARCHAR(50)),  
    CAST([SECTION] AS NVARCHAR(50)),  
    CAST([Year] AS NVARCHAR(10)),  
    CAST([CATEGROY] AS NVARCHAR(50)),  
    CAST([STRENGTH] AS NVARCHAR(20)),  
    CAST([Count_90_100] AS NVARCHAR(20)),  
    CAST([Count_80_90] AS NVARCHAR(20)),  
    CAST([Count_70_80] AS NVARCHAR(20)),  
    CAST([Count_60_70] AS NVARCHAR(20)),  
    CAST([Count_50_60] AS NVARCHAR(20)),  
    CAST([Count_40_50] AS NVARCHAR(20)),  
    CAST([Count_0_39] AS NVARCHAR(20)),  
    CAST([Above_70] AS NVARCHAR(20)),  
    CAST([Below_70] AS NVARCHAR(20)),  
    CAST([APPEARED] AS NVARCHAR(20)),  
    CAST([PASSED] AS NVARCHAR(20)),  
    CAST([PASS%] AS NVARCHAR(20)),  
    CAST([CLASS AVG] AS NVARCHAR(20)),  
    CAST([Position] AS NVARCHAR(50)),  
    CAST([TOTAL_POSITIONS] AS NVARCHAR(20)),  
    CAST([WL] AS NVARCHAR(20)),  
    CAST([SCHOOL-MERGE] AS NVARCHAR(255)),  
    CAST([SUBJECT_MERGE] AS NVARCHAR(255))  
FROM TR_ALL_SECTIONS_POS  

UNION  

SELECT DISTINCT  
    CAST([EID] AS NVARCHAR(50)),  
    CAST([NAME] AS NVARCHAR(255)),  
    CAST([SCHOOL] AS NVARCHAR(255)),  
    CASE WHEN [CATEGROY] = 'BOARD_ALL' THEN NULL ELSE CAST([SUBJECT] AS NVARCHAR(100)) END,  
    CAST([CLASS] AS NVARCHAR(50)),  
    CAST([SECTION] AS NVARCHAR(50)),  
    CAST([Year] AS NVARCHAR(10)),  
    CAST([CATEGROY] AS NVARCHAR(50)),  
    CAST([STRENGTH] AS NVARCHAR(20)),  
    CAST([Count_90_100] AS NVARCHAR(20)),  
    CAST([Count_80_90] AS NVARCHAR(20)),  
    CAST([Count_70_80] AS NVARCHAR(20)),  
    CAST([Count_60_70] AS NVARCHAR(20)),  
    CAST([Count_50_60] AS NVARCHAR(20)),  
    CAST([Count_40_50] AS NVARCHAR(20)),  
    CAST([Count_0_39] AS NVARCHAR(20)),  
    CAST([Above_70] AS NVARCHAR(20)),  
    CAST([Below_70] AS NVARCHAR(20)),  
    CAST([APPEARED] AS NVARCHAR(20)),  
    CAST([PASSED] AS NVARCHAR(20)),  
    CAST([PASS%] AS NVARCHAR(20)),  
    CAST([CLASS AVG] AS NVARCHAR(20)),  
    CAST([Position] AS NVARCHAR(50)),  
    CAST([TOTAL_POSITIONS] AS NVARCHAR(20)),  
    CAST([WL] AS NVARCHAR(20)),  
    CAST([SCHOOL-MERGE] AS NVARCHAR(255)),  
    CAST([SUBJECT_MERGE] AS NVARCHAR(255))  
FROM BOARD_MIDDLE  

UNION  

SELECT DISTINCT  
    CAST([EID] AS NVARCHAR(50)),  
    CAST([NAME] AS NVARCHAR(255)),  
    CAST([SCHOOL] AS NVARCHAR(255)),  
    CASE WHEN [CATEGROY] = 'BOARD_ALL' THEN NULL ELSE CAST([SUBJECT] AS NVARCHAR(100)) END,  
    CAST([CLASS] AS NVARCHAR(50)),  
    CAST([SECTION] AS NVARCHAR(50)),  
    CAST([Year] AS NVARCHAR(10)),  
    CAST([CATEGROY] AS NVARCHAR(50)),  
    CAST([STRENGTH] AS NVARCHAR(20)),  
    CAST([Count_90_100] AS NVARCHAR(20)),  
    CAST([Count_80_90] AS NVARCHAR(20)),  
    CAST([Count_70_80] AS NVARCHAR(20)),  
    CAST([Count_60_70] AS NVARCHAR(20)),  
    CAST([Count_50_60] AS NVARCHAR(20)),  
    CAST([Count_40_50] AS NVARCHAR(20)),  
    CAST([Count_0_39] AS NVARCHAR(20)),  
    CAST([Above_70] AS NVARCHAR(20)),  
    CAST([Below_70] AS NVARCHAR(20)),  
    CAST([APPEARED] AS NVARCHAR(20)),  
    CAST([PASSED] AS NVARCHAR(20)),  
    CAST([PASS%] AS NVARCHAR(20)),  
    CAST([CLASS AVG] AS NVARCHAR(20)),  
    CAST([Position] AS NVARCHAR(50)),  
    CAST([TOTAL_POSITIONS] AS NVARCHAR(20)),  
    CAST([WL] AS NVARCHAR(20)),  
    CAST([SCHOOL-MERGE] AS NVARCHAR(255)),  
    CAST([SUBJECT_MERGE] AS NVARCHAR(255))  
FROM ALL_BOARD_MIDDLE;

GO

-- View: [dbo].[ALL_COMBINED3] (Object ID: 651149365)
-- Created: 2025-06-19T12:43:15 | Modified: 2025-06-19T12:43:15
CREATE VIEW [dbo].[ALL_COMBINED3] AS
SELECT
    ac.*,
    CAST(AVG(bp.BOARD) AS NUMERIC(5, 2)) AS BOARD_PERCENTAGE
FROM ALL_COMBINED2 ac
LEFT JOIN BOARD_PER bp
    ON bp.SUBJECT = ac.SUBJECT
    AND bp.CLASS = TRY_CAST(ac.CLASS AS INT)
    AND bp.YEAR = TRY_CAST(ac.YEAR AS INT)
WHERE
    TRY_CAST(ac.CLASS AS INT) NOT IN (6, 7, 8)
    AND ac.SUBJECT IS NOT NULL
    AND LTRIM(RTRIM(ac.SUBJECT)) <> ''
    AND ac.YEAR IS NOT NULL
GROUP BY 
    ac.EID, ac.NAME, ac.SCHOOL, ac.SUBJECT, ac.CLASS, ac.SECTION, ac.YEAR, 
    ac.CATEGROY, ac.STRENGTH, ac.Count_90_100, ac.Count_80_90, ac.Count_70_80, 
    ac.Count_60_70, ac.Count_50_60, ac.Count_40_50, ac.Count_0_39, ac.Above_70, 
    ac.Below_70, ac.APPEARED, ac.PASSED, ac.[PASS%], ac.[CLASS AVG], ac.Position, 
    ac.TOTAL_POSITIONS, ac.WL, ac.[SCHOOL-MERGE], ac.SUBJECT_MERGE;

GO

-- View: [dbo].[BOARD_MIDDLE] (Object ID: 925246351)
-- Created: 2025-11-03T18:52:18.747 | Modified: 2025-11-03T19:22:16.807
CREATE VIEW [dbo].[BOARD_MIDDLE] AS

-- Function to retrieve a single Class Average value, preventing row duplication
-- This subquery is used in the SELECT list for both the BOARD and MIDDLE sections.
-- It is designed to return one value for a given EID and trimmed SUBJECT.
-- Note: You may need to replace DECIMAL(5,2) with a suitable numeric type for your system.

-- BOARD Summary Rows (Classes 9, 10, 11, 12)
SELECT 
    main.EID,
    MAX(main.NAME) AS NAME,
    MAX(main.SCHOOL) AS SCHOOL, 
    NULL AS EXAMTYPE,
    LTRIM(RTRIM(main.SUBJECT)) AS SUBJECT,
    NULL AS CLASS,
    NULL AS SECTION,
    NULL AS [Year],
    'BOARD' AS CATEGROY,
    MAX(main.[SCHOOL-MERGE]) AS [SCHOOL-MERGE],
    MAX(main.SUBJECT_MERGE) AS SUBJECT_MERGE,
    SUM(main.STRENGTH) AS STRENGTH,
    SUM(main.Count_90_100) AS Count_90_100,
    SUM(main.Count_80_90) AS Count_80_90,
    SUM(main.Count_70_80) AS Count_70_80,
    SUM(main.Count_60_70) AS Count_60_70,
    SUM(main.Count_50_60) AS Count_50_60,
    SUM(main.Count_40_50) AS Count_40_50,
    SUM(main.Count_0_39) AS Count_0_39,
    SUM(main.Above_70) AS Above_70,
    SUM(main.Below_70) AS Below_70,
    SUM(main.APPEARED) AS APPEARED,
    SUM(main.PASSED) AS PASSED,
    CAST(SUM(main.PASSED) * 100.0 / NULLIF(SUM(main.APPEARED), 0) AS DECIMAL(5,2)) AS [PASS%],
    
    -- SCALAR SUBQUERY: Replaces the problematic LEFT JOIN
    (SELECT TOP 1 CAST(ISNULL(v.[%], 0) AS DECIMAL(5,2)) 
     FROM vTeacher_sum_per_BOARD_MIDDLE v 
     WHERE v.EID = main.EID 
       AND LTRIM(RTRIM(v.SUBJECT)) = LTRIM(RTRIM(main.SUBJECT))
       AND v.CATEGROY = 'BOARD') AS [CLASS AVG],
       
    FLOOR(SUM(main.Position) * 1.0 / NULLIF(COUNT(main.Position), 0)) AS Position,
    FLOOR(SUM(main.TOTAL_POSITIONS) * 1.0 / NULLIF(COUNT(main.TOTAL_POSITIONS), 0)) AS TOTAL_POSITIONS,
    FLOOR(SUM(main.WL) * 1.0 / NULLIF(COUNT(main.WL), 0)) AS WL
FROM 
    TR_ALL_SECTIONS_POS main
WHERE 
    main.CLASS IN (9, 10, 11, 12)
    AND main.EXAMTYPE = 'ANNUAL'
GROUP BY 
    main.EID, LTRIM(RTRIM(main.SUBJECT)), main.SCHOOL 

UNION ALL

-- MIDDLE Summary Rows (Classes 6, 7, 8)
SELECT 
    main.EID,
    MAX(main.NAME) AS NAME,
    MAX(main.SCHOOL) AS SCHOOL, 
    NULL AS EXAMTYPE,
    LTRIM(RTRIM(main.SUBJECT)) AS SUBJECT,
    NULL AS CLASS,
    NULL AS SECTION,
    NULL AS [Year],
    'MIDDLE' AS CATEGROY,
    MAX(main.[SCHOOL-MERGE]) AS [SCHOOL-MERGE],
    MAX(main.SUBJECT_MERGE) AS SUBJECT_MERGE,
    SUM(main.STRENGTH) AS STRENGTH,
    SUM(main.Count_90_100) AS Count_90_100,
    SUM(main.Count_80_90) AS Count_80_90,
    SUM(main.Count_70_80) AS Count_70_80,
    SUM(main.Count_60_70) AS Count_60_70,
    SUM(main.Count_50_60) AS Count_50_60,
    SUM(main.Count_40_50) AS Count_40_50,
    SUM(main.Count_0_39) AS Count_0_39,
    SUM(main.Above_70) AS Above_70,
    SUM(main.Below_70) AS Below_70,
    SUM(main.APPEARED) AS APPEARED,
    SUM(main.PASSED) AS PASSED,
    CAST(SUM(main.PASSED) * 100.0 / NULLIF(SUM(main.APPEARED), 0) AS DECIMAL(5,2)) AS [PASS%],
    
    -- SCALAR SUBQUERY: Replaces the problematic LEFT JOIN
    (SELECT TOP 1 CAST(ISNULL(v.[%], 0) AS DECIMAL(5,2)) 
     FROM vTeacher_sum_per_BOARD_MIDDLE v 
     WHERE v.EID = main.EID 
       AND LTRIM(RTRIM(v.SUBJECT)) = LTRIM(RTRIM(main.SUBJECT))
       AND v.CATEGROY = 'MIDDLE') AS [CLASS AVG],
       
    FLOOR(SUM(main.Position) * 1.0 / NULLIF(COUNT(main.Position), 0)) AS Position,
    FLOOR(SUM(main.TOTAL_POSITIONS) * 1.0 / NULLIF(COUNT(main.TOTAL_POSITIONS), 0)) AS TOTAL_POSITIONS,
    FLOOR(SUM(main.WL) * 1.0 / NULLIF(COUNT(main.WL), 0)) AS WL
FROM 
    TR_ALL_SECTIONS_POS main
WHERE 
    main.CLASS IN (6, 7, 8)
    AND main.EXAMTYPE = 'ANNUAL'
GROUP BY 
    main.EID, LTRIM(RTRIM(main.SUBJECT)), main.SCHOOL;

GO

-- View: [dbo].[BOARD_MIDDLE_CORRECTED] (Object ID: 765245781)
-- Created: 2025-10-31T09:15:22.057 | Modified: 2025-10-31T09:15:22.057
CREATE VIEW [dbo].[BOARD_MIDDLE_CORRECTED]
AS
WITH Base AS (
    SELECT
        EID,
        NAME,
        SCHOOL,
        EXAMTYPE,
        SUBJECT,
        TRY_CAST([CLASS] AS INT) AS CLASS_INT,
        [SECTION],
        [Year],
        CASE
            WHEN TRY_CAST([CLASS] AS INT) BETWEEN 6 AND 8 THEN 'MIDDLE'
            WHEN TRY_CAST([CLASS] AS INT) BETWEEN 9 AND 12 THEN 'BOARD'
            ELSE COALESCE([CATEGROY], 'UNKNOWN')
        END AS CATEGROY_FIXED,
        COALESCE([STRENGTH], 0) AS STRENGTH,
        COALESCE([APPEARED], 0) AS APPEARED,
        COALESCE([PASSED], 0) AS PASSED,
        COALESCE([Count_90_100], 0) AS Count_90_100,
        COALESCE([Count_80_90], 0) AS Count_80_90,
        COALESCE([Count_70_80], 0) AS Count_70_80,
        COALESCE([Count_60_70], 0) AS Count_60_70,
        COALESCE([Count_50_60], 0) AS Count_50_60,
        COALESCE([Count_40_50], 0) AS Count_40_50,
        COALESCE([Count_0_39], 0) AS Count_0_39,
        COALESCE([Above_70], 0) AS Above_70,
        COALESCE([Below_70], 0) AS Below_70,
        COALESCE([CLASS AVG], 0) AS CLASS_AVG
    FROM dbo.TR_ALL_SECTIONS_POS
),

PerSchool AS (
    SELECT
        CATEGROY_FIXED,
        SUBJECT,
        SCHOOL,
        SUM(STRENGTH)        AS School_Strength,
        SUM(APPEARED)        AS School_Appeared,
        SUM(PASSED)          AS School_Passed,
        SUM(Count_90_100)    AS School_Count_90_100,
        SUM(Count_80_90)     AS School_Count_80_90,
        SUM(Count_70_80)     AS School_Count_70_80,
        SUM(Count_60_70)     AS School_Count_60_70,
        SUM(Count_50_60)     AS School_Count_50_60,
        SUM(Count_40_50)     AS School_Count_40_50,
        SUM(Count_0_39)      AS School_Count_0_39,
        SUM(Above_70)        AS School_Above_70,
        SUM(Below_70)        AS School_Below_70,
        AVG(CLASS_AVG)       AS School_CLASS_AVG
    FROM Base
    GROUP BY CATEGROY_FIXED, SUBJECT, SCHOOL
),

FinalAgg AS (
    SELECT
        SUBJECT,
        CATEGROY_FIXED AS CATEGROY,
        STRING_AGG(SCHOOL, '-') WITHIN GROUP (ORDER BY SCHOOL) AS [SCHOOL-MERGE],
        SUM(School_Strength)    AS [STRENGTH],
        SUM(School_Appeared)    AS [APPEARED],
        SUM(School_Passed)      AS [PASSED],
        SUM(School_Count_90_100)AS [Count_90_100],
        SUM(School_Count_80_90) AS [Count_80_90],
        SUM(School_Count_70_80) AS [Count_70_80],
        SUM(School_Count_60_70) AS [Count_60_70],
        SUM(School_Count_50_60) AS [Count_50_60],
        SUM(School_Count_40_50) AS [Count_40_50],
        SUM(School_Count_0_39)  AS [Count_0_39],
        SUM(School_Above_70)    AS [Above_70],
        SUM(School_Below_70)    AS [Below_70],
        AVG(School_CLASS_AVG)   AS [CLASS AVG]
    FROM PerSchool
    GROUP BY SUBJECT, CATEGROY_FIXED
)

SELECT
    ROW_NUMBER() OVER (ORDER BY SUBJECT, CATEGROY) AS RowNo,
    SUBJECT,
    [SCHOOL-MERGE],
    CATEGROY,
    [STRENGTH],
    [APPEARED],
    [PASSED],
    [CLASS AVG],
    [Count_90_100],
    [Count_80_90],
    [Count_70_80],
    [Count_60_70],
    [Count_50_60],
    [Count_40_50],
    [Count_0_39],
    [Above_70],
    [Below_70]
FROM FinalAgg;

GO

-- View: [dbo].[BOARD_MIDDLE_WORKING] (Object ID: 381244413)
-- Created: 2025-10-24T08:37:41.677 | Modified: 2025-11-03T19:22:11.333
CREATE VIEW [dbo].[BOARD_MIDDLE_WORKING] AS

-- BOARD Summary Rows
SELECT 
    main.EID,
    MAX(main.NAME) AS NAME,
    MAX(main.SCHOOL) AS SCHOOL,
    NULL AS EXAMTYPE,
    main.SUBJECT,
    NULL AS CLASS,
    NULL AS SECTION,
    NULL AS Year,
    'BOARD' AS CATEGROY,
    MAX(main.[SCHOOL-MERGE]) AS [SCHOOL-MERGE],
    MAX(main.SUBJECT_MERGE) AS SUBJECT_MERGE,
    SUM(main.STRENGTH) AS STRENGTH,
    SUM(main.Count_90_100) AS Count_90_100,
    SUM(main.Count_80_90) AS Count_80_90,
    SUM(main.Count_70_80) AS Count_70_80,
    SUM(main.Count_60_70) AS Count_60_70,
    SUM(main.Count_50_60) AS Count_50_60,
    SUM(main.Count_40_50) AS Count_40_50,
    SUM(main.Count_0_39) AS Count_0_39,
    SUM(main.Above_70) AS Above_70,
    SUM(main.Below_70) AS Below_70,
    SUM(main.APPEARED) AS APPEARED,
    SUM(main.PASSED) AS PASSED,
    CAST(SUM(main.PASSED) * 100.0 / NULLIF(SUM(main.APPEARED), 0) AS DECIMAL(5,2)) AS [PASS%],
    CAST(MAX(ISNULL(v.[%], 0)) AS DECIMAL(5,2)) AS [CLASS AVG],  -- use value from vTeacher_sum_per_BOARD_MIDDLE
    FLOOR(SUM(main.Position) * 1.0 / NULLIF(COUNT(main.Position), 0)) AS Position,
    FLOOR(SUM(main.TOTAL_POSITIONS) * 1.0 / NULLIF(COUNT(main.TOTAL_POSITIONS), 0)) AS TOTAL_POSITIONS,
    FLOOR(SUM(main.WL) * 1.0 / NULLIF(COUNT(main.WL), 0)) AS WL
FROM 
    TR_ALL_SECTIONS_POS main
    LEFT JOIN vTeacher_sum_per_BOARD_MIDDLE v 
        ON v.EID = main.EID 
        AND v.SUBJECT = main.SUBJECT
        AND v.CATEGROY = 'BOARD'
WHERE 
    main.CLASS IN (9, 10, 11, 12)
GROUP BY 
    main.EID, main.SUBJECT

UNION ALL

-- MIDDLE Summary Rows
SELECT 
    main.EID,
    MAX(main.NAME) AS NAME,
    MAX(main.SCHOOL) AS SCHOOL,
    NULL AS EXAMTYPE,
    main.SUBJECT,
    NULL AS CLASS,
    NULL AS SECTION,
    NULL AS Year,
    'MIDDLE' AS CATEGROY,
    MAX(main.[SCHOOL-MERGE]) AS [SCHOOL-MERGE],
    MAX(main.SUBJECT_MERGE) AS SUBJECT_MERGE,
    SUM(main.STRENGTH) AS STRENGTH,
    SUM(main.Count_90_100) AS Count_90_100,
    SUM(main.Count_80_90) AS Count_80_90,
    SUM(main.Count_70_80) AS Count_70_80,
    SUM(main.Count_60_70) AS Count_60_70,
    SUM(main.Count_50_60) AS Count_50_60,
    SUM(main.Count_40_50) AS Count_40_50,
    SUM(main.Count_0_39) AS Count_0_39,
    SUM(main.Above_70) AS Above_70,
    SUM(main.Below_70) AS Below_70,
    SUM(main.APPEARED) AS APPEARED,
    SUM(main.PASSED) AS PASSED,
    CAST(SUM(main.PASSED) * 100.0 / NULLIF(SUM(main.APPEARED), 0) AS DECIMAL(5,2)) AS [PASS%],
    CAST(MAX(ISNULL(v.[%], 0)) AS DECIMAL(5,2)) AS [CLASS AVG],  -- use value from vTeacher_sum_per_BOARD_MIDDLE
    FLOOR(SUM(main.Position) * 1.0 / NULLIF(COUNT(main.Position), 0)) AS Position,
    FLOOR(SUM(main.TOTAL_POSITIONS) * 1.0 / NULLIF(COUNT(main.TOTAL_POSITIONS), 0)) AS TOTAL_POSITIONS,
    FLOOR(SUM(main.WL) * 1.0 / NULLIF(COUNT(main.WL), 0)) AS WL
FROM 
    TR_ALL_SECTIONS_POS main
    LEFT JOIN vTeacher_sum_per_BOARD_MIDDLE v 
        ON v.EID = main.EID 
        AND v.SUBJECT = main.SUBJECT
        AND v.CATEGROY = 'MIDDLE'
WHERE 
    main.CLASS IN (6, 7, 8)
GROUP BY 
    main.EID, main.SUBJECT;

GO

-- View: [dbo].[BOARD_MIDDLE_old] (Object ID: 1710629137)
-- Created: 2025-06-03T20:03:50.793 | Modified: 2025-10-24T08:41:04.040
-- Create view with BOARD and MIDDLE summary rows, one per EID and SUBJECT using TR_ALL_SECTIONS_POS
CREATE VIEW [dbo].[BOARD_MIDDLE_old] AS

-- BOARD Summary Rows
SELECT
    EID,
    MAX(NAME) AS NAME,
    MAX(SCHOOL) AS SCHOOL,
    NULL AS EXAMTYPE,
    SUBJECT,
    NULL AS CLASS,
    NULL AS SECTION,
    NULL AS Year,
    'BOARD' AS CATEGROY,
    MAX([SCHOOL-MERGE]) AS [SCHOOL-MERGE],
    MAX(SUBJECT_MERGE) AS SUBJECT_MERGE,
    SUM(STRENGTH) AS STRENGTH,
    SUM(Count_90_100) AS Count_90_100,
    SUM(Count_80_90) AS Count_80_90,
    SUM(Count_70_80) AS Count_70_80,
    SUM(Count_60_70) AS Count_60_70,
    SUM(Count_50_60) AS Count_50_60,
    SUM(Count_40_50) AS Count_40_50,
    SUM(Count_0_39) AS Count_0_39,
    SUM(Above_70) AS Above_70,
    SUM(Below_70) AS Below_70,
    SUM(APPEARED) AS APPEARED,
    SUM(PASSED) AS PASSED,
    CAST(SUM(PASSED) * 100.0 / NULLIF(SUM(APPEARED), 0) AS DECIMAL(5,2)) AS [PASS%],
    CAST(SUM([CLASS AVG]) / NULLIF(COUNT([CLASS AVG]), 0) AS DECIMAL(5,2)) AS [CLASS AVG],
    FLOOR(SUM(Position) * 1.0 / NULLIF(COUNT(Position), 0)) AS Position,
    FLOOR(SUM(TOTAL_POSITIONS) * 1.0 / NULLIF(COUNT(TOTAL_POSITIONS), 0)) AS TOTAL_POSITIONS,
    FLOOR(SUM(WL) * 1.0 / NULLIF(COUNT(WL), 0)) AS WL
FROM TR_ALL_SECTIONS_POS main
WHERE CLASS IN (9,10,11,12)
GROUP BY EID, SUBJECT

UNION ALL

-- MIDDLE Summary Rows
SELECT
    EID,
    MAX(NAME) AS NAME,
    MAX(SCHOOL) AS SCHOOL,
    NULL AS EXAMTYPE,
    SUBJECT,
    NULL AS CLASS,
    NULL AS SECTION,
    NULL AS Year,
    'MIDDLE' AS CATEGROY,
    MAX([SCHOOL-MERGE]) AS [SCHOOL-MERGE],
    MAX(SUBJECT_MERGE) AS SUBJECT_MERGE,
    SUM(STRENGTH) AS STRENGTH,
    SUM(Count_90_100) AS Count_90_100,
    SUM(Count_80_90) AS Count_80_90,
    SUM(Count_70_80) AS Count_70_80,
    SUM(Count_60_70) AS Count_60_70,
    SUM(Count_50_60) AS Count_50_60,
    SUM(Count_40_50) AS Count_40_50,
    SUM(Count_0_39) AS Count_0_39,
    SUM(Above_70) AS Above_70,
    SUM(Below_70) AS Below_70,
    SUM(APPEARED) AS APPEARED,
    SUM(PASSED) AS PASSED,
    CAST(SUM(PASSED) * 100.0 / NULLIF(SUM(APPEARED), 0) AS DECIMAL(5,2)) AS [PASS%],
    CAST(SUM([CLASS AVG]) / NULLIF(COUNT([CLASS AVG]), 0) AS DECIMAL(5,2)) AS [CLASS AVG],
    FLOOR(SUM(Position) * 1.0 / NULLIF(COUNT(Position), 0)) AS Position,
    FLOOR(SUM(TOTAL_POSITIONS) * 1.0 / NULLIF(COUNT(TOTAL_POSITIONS), 0)) AS TOTAL_POSITIONS,
    FLOOR(SUM(WL) * 1.0 / NULLIF(COUNT(WL), 0)) AS WL
FROM TR_ALL_SECTIONS_POS main
WHERE CLASS IN (6,7,8)
GROUP BY EID, SUBJECT;

GO

-- View: [dbo].[CC_ALL] (Object ID: 1806629479)
-- Created: 2025-06-10T23:49:38.530 | Modified: 2025-06-10T23:49:38.530
CREATE VIEW [dbo].[CC_ALL] AS
WITH TeacherCategory AS (
    SELECT 
        EID,
        MAX(CASE WHEN CATEGROY = 'BOARD' THEN 1 ELSE 0 END) AS HasBoard,
        MAX(CASE WHEN CATEGROY = 'MIDDLE' THEN 1 ELSE 0 END) AS HasMiddle
    FROM COUNT_CAT
    GROUP BY EID
),
ClassTypeMapping AS (
    SELECT 
        E.EID,
        E.NAME,  -- Ensure NAME column exists in COUNT_CAT
        CASE 
            WHEN T.HasBoard = 1 AND T.HasMiddle = 1 THEN 'BOARD + MIDDLE'
            WHEN T.HasBoard = 1 AND T.HasMiddle = 0 THEN 'BOARD'
            WHEN T.HasBoard = 0 AND T.HasMiddle = 1 THEN 'MIDDLE'
        END AS [CLASS TYPE],
        E.SCHOOL,
        E.[CLASS AVG - DED]
    FROM COUNT_CAT E
    JOIN TeacherCategory T ON E.EID = T.EID
),
UniqueEIDs AS (
    SELECT 
        [CLASS TYPE], 
        SCHOOL, 
        EID, 
        NAME,
        MAX([CLASS AVG - DED]) AS [CLASS AVG - DED]
    FROM ClassTypeMapping
    GROUP BY [CLASS TYPE], SCHOOL, EID, NAME
),
Scored AS (
    SELECT
        [CLASS TYPE],
        SCHOOL,
        CASE 
            WHEN [CLASS AVG - DED] >= 90 THEN '90-100'
            WHEN [CLASS AVG - DED] >= 80 THEN '80-89'
            WHEN [CLASS AVG - DED] >= 70 THEN '70-79'
            WHEN [CLASS AVG - DED] >= 60 THEN '60-69'
            ELSE '0-59'
        END AS CATEGORIES,
        EID,
        NAME
    FROM UniqueEIDs
),
FinalSummary AS (
    SELECT
        [CLASS TYPE],
        CATEGORIES,
        SCHOOL,
        EID,
        NAME
    FROM Scored
)
SELECT *,
    COUNT(EID) OVER (PARTITION BY [CLASS TYPE], SCHOOL, CATEGORIES) AS [NO OF TEACHERS],
    COUNT(EID) OVER (PARTITION BY [CLASS TYPE], SCHOOL) AS [TOTAL TEACHERS]
FROM FinalSummary;

GO

-- View: [dbo].[COUNT_CAT] (Object ID: 1790629422)
-- Created: 2025-06-10T21:04:59.300 | Modified: 2025-06-10T21:05:57.707
CREATE   VIEW [dbo].[COUNT_CAT] AS
WITH DistinctSubjects AS (
    SELECT 
        EID,
        NAME,
        SCHOOL,
        CASE 
            WHEN CLASS IN ('9','10','11','12') THEN 'BOARD'
            WHEN CLASS IN ('6','7','8') THEN 'MIDDLE'
        END AS CATEGROY,
        CASE SUBJECT
            WHEN 'Mathematics' THEN 'Math'
            WHEN 'GENERAL Science' THEN 'Sci'
            WHEN 'English' THEN 'Eng'
            WHEN 'Computer Science' THEN 'CS'
            WHEN 'Biology' THEN 'Bio'
            WHEN 'Physics' THEN 'Phy'
            WHEN 'Chemistry' THEN 'Chem'
            WHEN 'PAKISTAN STUDIES' THEN 'PST'
            WHEN 'SOCIAL STUDIES' THEN 'SST'
			WHEN 'URDU' THEN 'URD'
            WHEN 'ISLAMIYAT' THEN 'ISL'
            WHEN 'TRANSLATION OF THE HOLY QURAN' THEN 'TJQ'
			 WHEN 'ISLAMIC EDUCATION' THEN 'ISE'
            ELSE SUBJECT
        END AS SUBJECT_ABBR
    FROM TR_ALL_DEDUCTED
    WHERE CLASS IN ('6','7','8','9','10','11','12')
    GROUP BY EID, NAME, SCHOOL, CLASS, SUBJECT
),
SubjectAgg AS (
    SELECT 
        EID,
        CATEGROY,
        STRING_AGG(SUBJECT_ABBR, '-') AS SUBJECTS
    FROM (
        SELECT DISTINCT EID, CATEGROY, SUBJECT_ABBR
        FROM DistinctSubjects
    ) AS UniqueSubjects
    GROUP BY EID, CATEGROY
),
BaseData AS (
    SELECT
        EID,
        NAME,
        SCHOOL,
        SUBJECT,
        CLASS,
        STRENGTH,
        APPEARED,
        PASSED,
        FAIL,
        [CLASS AVG],
        DEDUCTION,
        CASE 
            WHEN CLASS IN ('9','10','11','12') THEN 'BOARD'
            WHEN CLASS IN ('6','7','8') THEN 'MIDDLE'
        END AS CATEGROY
    FROM TR_ALL_DEDUCTED
    WHERE CLASS IN ('6','7','8','9','10','11','12')
)
SELECT
    A.EID,
    A.NAME,
    A.SCHOOL,
    S.SUBJECTS AS SUBJECT,
    A.CATEGROY,
    SUM(A.STRENGTH) AS STRENGTH,
    SUM(A.APPEARED) AS APPEARED,
    SUM(A.PASSED) AS PASSED,
    SUM(A.FAIL) AS FAIL,
    AVG(A.[CLASS AVG]) AS [CLASS AVG],
    SUM(A.DEDUCTION) AS DEDUCTION,
    AVG(A.[CLASS AVG]) - SUM(A.DEDUCTION) AS [CLASS AVG - DED]
FROM BaseData A
JOIN SubjectAgg S ON A.EID = S.EID AND A.CATEGROY = S.CATEGROY
GROUP BY A.EID, A.NAME, A.SCHOOL, A.CATEGROY, S.SUBJECTS;

GO

-- View: [dbo].[Data_Entry_Status_View] (Object ID: 758293761)
-- Created: 2025-12-14T18:22:51.703 | Modified: 2026-01-31T00:17:04.670
CREATE VIEW [dbo].[Data_Entry_Status_View]
AS
SELECT
    SRE.SCHOOL,
    TIE.NAME AS TEACHER,
    SRE.CLASS,
    SRE.SECTION,
    -- We group by the section broadly to catch mixed groups
    SRE.[GROUP], 
    TIE.SUBJECT,
    TIE.EXAM AS EXAMTYPE,
    SRE.YEAR,
    COUNT(SRE.ROLLNO) AS TOTALCOUNT,
    COUNT(MI.OBTAINED) AS ENTRIES_MARKED,
    ISNULL(CAST((COUNT(MI.OBTAINED) * 100.0) / NULLIF(COUNT(SRE.ROLLNO), 0) AS DECIMAL(10, 2)), 0.00) AS [INPUTCOMPLETED %],
    ISNULL(CAST((SUM(ISNULL(MI.OBTAINED, 0)) * 100.0) / NULLIF(SUM(ISNULL(MI.TOTAL, 0)), 0) AS DECIMAL(10, 2)), 0.00) AS [RESULTCOMPLETED %]
FROM STUDENTS_ROLL_INTERNAL_EXAM AS SRE
INNER JOIN teachers_internal_exam AS TIE
    ON SRE.CLASS = TIE.CLASS
    AND SRE.SECTION = TIE.SECTION
    AND SRE.SCHOOL = TIE.SCHOOL
    AND SRE.EXAM = TIE.EXAM
    -- Removed Group from JOIN to allow the Teacher's Subject to find all students in the Section
LEFT JOIN Marks_Internal AS MI
    ON SRE.ROLLNO = MI.ROLLNO
    AND TIE.SUBJECT = MI.SUBJECT 
    AND SRE.CLASS = MI.CLASS 
    AND TIE.EXAM = MI.EXAMTYPE
GROUP BY 
    SRE.SCHOOL, TIE.NAME, SRE.CLASS, SRE.SECTION, SRE.[GROUP], TIE.SUBJECT, TIE.EXAM, SRE.YEAR;

GO

-- View: [dbo].[GZT_CR] (Object ID: 2030630277)
-- Created: 2025-06-14T19:18:51.460 | Modified: 2025-06-15T11:47:01.333
CREATE VIEW [dbo].[GZT_CR] AS
SELECT 
    gs.*, 
    gs.count - ISNULL(sr.student_count, 0) AS difference
FROM 
    GZT_STRENGTH gs
OUTER APPLY (
    SELECT COUNT(*) AS student_count
    FROM STUDENTS_ROLL sr
    WHERE sr.SCHOOL = gs.SCHOOL 
      AND sr.YEAR = gs.YEAR 
      AND sr.CLASS = gs.CLASS
) sr;

GO

-- View: [dbo].[HOF_FRMT] (Object ID: 663673412)
-- Created: 2025-07-17T15:47:31.297 | Modified: 2025-07-17T15:47:31.297
CREATE VIEW [dbo].[HOF_FRMT] AS
SELECT DISTINCT
    T.EID,
    T.NAME,
    T.SUBJECT,
    T.SCHOOL,
    T.Year,
    CAST(T.Class AS VARCHAR(10)) + '/' + T.Section AS [CLASS/SECTION],
    T.APPEARED,
    FORMAT(T.[PASS%], 'N2') AS [PASS%],
    -- PASS% OF BOARD with detailed join keys
    CASE 
        WHEN T.Class IN (9,10,11,12) THEN FORMAT(A.BOARD_PERCENTAGE, 'N2')
        ELSE NULL
    END AS [PASS% OF BOARD],
    T.Position,
    T.TOTAL_POSITIONS,
    T.WL AS [WORK LOAD],
    T.[CLASS AVG],
    T.Count_90_100 AS [ABOVE 90%],
    T.Count_80_90 AS [ABOVE 80%],
    T.Count_70_80 AS [ABOVE 70%],
    T.Count_60_70 AS [ABOVE 60%],
    T.Count_50_60 AS [ABOVE 50%],
    T.Count_40_50 AS [ABOVE 40%],
    T.Count_0_39 AS [BELOW 40%],
    -- % of students securing more than 70%
    FORMAT(
        CASE WHEN T.APPEARED > 0 THEN CAST(T.ABOVE_70 AS FLOAT) / T.APPEARED * 100 ELSE NULL END, 'N2'
    ) AS [ABOVE 70 %],
    T.ABOVE_70 AS [ABOVE 70 COUNT],
    -- % of students securing less than 70%
    FORMAT(
        CASE WHEN T.APPEARED > 0 THEN CAST(T.BELOW_70 AS FLOAT) / T.APPEARED * 100 ELSE NULL END, 'N2'
    ) AS [BELOW 70 %],
    T.BELOW_70 AS [BELOW 70% COUNT],
    -- Blank Remarks
    '' AS [REMARKS]
FROM
    TR_ALL_IND_POS T
    LEFT JOIN ALL_COMBINED3 A
        ON T.Year = A.Year
        AND T.Class = A.Class
        AND T.Subject = A.Subject
        AND T.EID = A.EID
        AND T.School = A.School
        AND T.Class IN (9,10,11,12);

GO

-- View: [dbo].[HOF_FRMT2] (Object ID: 695673526)
-- Created: 2025-07-17T17:57:26.887 | Modified: 2025-07-17T17:57:26.887
CREATE VIEW [dbo].[HOF_FRMT2] AS
SELECT DISTINCT
    T.EID,
    T.NAME,
    T.SUBJECT,
    T.SCHOOL,
    T.Year,
    CAST(T.Class AS VARCHAR(10)) + '/' + T.Section AS [CLASS/SECTION],
    T.APPEARED,
    T.PASSED,  -- Added column
    FORMAT(T.[PASS%], 'N2') AS [PASS%],
    -- PASS% OF BOARD with detailed join keys
    CASE 
        WHEN T.Class IN (9,10,11,12) THEN FORMAT(A.BOARD_PERCENTAGE, 'N2')
        ELSE NULL
    END AS [PASS% OF BOARD],
    T.Position,
    T.TOTAL_POSITIONS,
    T.WL AS [WORK LOAD],
    T.[CLASS AVG],
    T.Count_90_100 AS [ABOVE 90%],
    T.Count_80_90 AS [ABOVE 80%],
    T.Count_70_80 AS [ABOVE 70%],
    T.Count_60_70 AS [ABOVE 60%],
    T.Count_50_60 AS [ABOVE 50%],
    T.Count_40_50 AS [ABOVE 40%],
    T.Count_0_39 AS [BELOW 40%],
    -- % of students securing more than 70%
    FORMAT(
        CASE WHEN T.APPEARED > 0 THEN CAST(T.ABOVE_70 AS FLOAT) / T.APPEARED * 100 ELSE NULL END, 'N2'
    ) AS [ABOVE 70 %],
    T.ABOVE_70 AS [ABOVE 70 COUNT],
    -- % of students securing less than 70%
    FORMAT(
        CASE WHEN T.APPEARED > 0 THEN CAST(T.BELOW_70 AS FLOAT) / T.APPEARED * 100 ELSE NULL END, 'N2'
    ) AS [BELOW 70 %],
    T.BELOW_70 AS [BELOW 70% COUNT],
    -- Blank Remarks
    '' AS [REMARKS]
FROM
    TR_ALL_IND_POS T
    LEFT JOIN ALL_COMBINED3 A
        ON T.Year = A.Year
        AND T.Class = A.Class
        AND T.Subject = A.Subject
        AND T.EID = A.EID
        AND T.School = A.School
        AND T.Class IN (9,10,11,12);

GO

-- View: [dbo].[INTERNAL_CONSOLIDATED_RESULT_SHEET_VIEW] (Object ID: 1430296155)
-- Created: 2025-12-18T16:43:08.577 | Modified: 2026-05-06T08:05:03.047
CREATE VIEW [dbo].[INTERNAL_CONSOLIDATED_RESULT_SHEET_VIEW] AS
WITH SubjectPivot AS (
    SELECT 
        ROLLNO, 
        EXAMTYPE, 
        YEAR,
        MAX(CASE WHEN SUBJECT = 'CHEMISTRY' THEN OBTAINED END) AS [CHEMISTRY],
        MAX(CASE WHEN SUBJECT = 'COMPUTER SCIENCE' THEN OBTAINED END) AS [COMPUTER SCIENCE],
        MAX(CASE WHEN SUBJECT = 'GENERAL SCIENCE' THEN OBTAINED END) AS [GENERAL SCIENCE],
        MAX(CASE WHEN SUBJECT = 'ENGLISH' THEN OBTAINED END) AS [ENGLISH],
        MAX(CASE WHEN SUBJECT = 'ISLAMIC EDUCATION' THEN OBTAINED END) AS [ISLAMIC EDUCATION],
        MAX(CASE WHEN SUBJECT = 'ISLAMIYAT' THEN OBTAINED END) AS [ISLAMIYAT],
        MAX(CASE WHEN SUBJECT = 'MATHEMATICS' THEN OBTAINED END) AS [MATHEMATICS],
        MAX(CASE WHEN SUBJECT = 'PAKISTAN STUDIES' THEN OBTAINED END) AS [PAKISTAN STUDIES],
        MAX(CASE WHEN SUBJECT = 'PHYSICS' THEN OBTAINED END) AS [PHYSICS],
        MAX(CASE WHEN SUBJECT = 'TRANSLATION OF THE HOLY QURAN' THEN OBTAINED END) AS [TRANSLATION OF THE HOLY QURAN],
        MAX(CASE WHEN SUBJECT = 'URDU' THEN OBTAINED END) AS [URDU],
        MAX(CASE WHEN SUBJECT = 'BIOLOGY' THEN OBTAINED END) AS [BIOLOGY],
        MAX(CASE WHEN SUBJECT = 'SOCIAL STUDIES' THEN OBTAINED END) AS [SOCIAL STUDIES],
        MAX(CASE WHEN SUBJECT = 'ARTS' THEN OBTAINED END) AS [ARTS]
    FROM MARKS_INTERNAL
    GROUP BY ROLLNO, EXAMTYPE, YEAR
)
SELECT 
    S.SCHOOL,
    S.STUDENT,        
    S.FATHER,         
    S.CLASS,
    S.SECTION,
    S.YEAR,
    S.SMSNO,
    
    -- *** THIS IS THE UPDATED LINE ***
    -- Converts scientific notation to a full numeric string (e.g., 1426110888)
    CAST(CAST(TRY_CAST(S.ROLLNO AS FLOAT) AS DECIMAL(38,0)) AS VARCHAR(50)) AS ROLLNO,
    
    S.[GROUP],
    P.EXAMTYPE AS EXAM, 
    P.[CHEMISTRY],
    P.[COMPUTER SCIENCE],
    P.[GENERAL SCIENCE],
    P.[ENGLISH],
    P.[ISLAMIC EDUCATION],
    P.[ISLAMIYAT],
    P.[MATHEMATICS],
    P.[PAKISTAN STUDIES],
    P.[PHYSICS],
    P.[TRANSLATION OF THE HOLY QURAN],
    P.[URDU],
    P.[BIOLOGY],
    P.[SOCIAL STUDIES],
    P.[ARTS],
    R.GrandObtained AS SUM_OBTAINED,
    R.GrandTotal AS SUM_TOTAL,
    R.OverallPercentage AS [%],
    
    -- --- DYNAMIC FINAL STATUS LOGIC ---
    CASE 
        WHEN EXISTS (SELECT 1 FROM MARKS_INTERNAL M 
                     WHERE M.ROLLNO = S.ROLLNO AND M.STATUS = 'FAIL' 
                     AND M.EXAMTYPE = P.EXAMTYPE AND M.YEAR = S.YEAR) 
        THEN 'FAIL' 
        ELSE 'PASS' 
    END AS FINAL_STATUS,

    -- --- UPDATED GRADING LOGIC BY CLASS LEVEL ---
    CASE 
        -- Logic for Middle School (Class 6, 7, 8) - Minimum 40% for E
        WHEN S.CLASS IN ('6', '7', '8') THEN
            CASE 
                WHEN R.OverallPercentage >= 90 THEN 'A+'
                WHEN R.OverallPercentage >= 80 THEN 'A'
                WHEN R.OverallPercentage >= 70 THEN 'B'
                WHEN R.OverallPercentage >= 60 THEN 'C'
                WHEN R.OverallPercentage >= 50 THEN 'D'
                WHEN R.OverallPercentage >= 40 THEN 'E'
                ELSE 'F'
            END
        -- Logic for Senior/Inter (Class 9, 10, 11, 12) - Minimum 33% for E
        WHEN S.CLASS IN ('9', '10', '11', '12') THEN
            CASE 
                WHEN R.OverallPercentage >= 90 THEN 'A+'
                WHEN R.OverallPercentage >= 80 THEN 'A'
                WHEN R.OverallPercentage >= 70 THEN 'B'
                WHEN R.OverallPercentage >= 60 THEN 'C'
                WHEN R.OverallPercentage >= 50 THEN 'D'
                WHEN R.OverallPercentage >= 33 THEN 'E'
                ELSE 'F'
            END
        ELSE 'F' -- Default fallback
    END AS GRADE,

    R.PositionInSection AS [POSITION in section],
    R.PositionInClass AS [position in class]
FROM STUDENTS_ROLL_INTERNAL_EXAM S
INNER JOIN SubjectPivot P ON S.ROLLNO = P.ROLLNO 
                          AND S.YEAR = P.YEAR 
                          AND S.EXAM = P.EXAMTYPE 
LEFT JOIN INTERNAL_STUDENT_SUMMARY_RANKS R ON S.ROLLNO = R.ROLLNO 
    AND R.EXAMTYPE = P.EXAMTYPE 
    AND R.YEAR = S.YEAR;

GO

-- View: [dbo].[INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW] (Object ID: 1094294958)
-- Created: 2025-12-17T03:11:40.777 | Modified: 2026-02-08T22:35:17.167
CREATE   VIEW [dbo].[INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW] AS
SELECT 
    T.ID,
    T.SCHOOL,
    T.EXAM AS EXAMTYPE,
    T.EID,
    T.NAME AS [TEACHER NAME],
    T.YEAR,
    T.CLASS,
    T.SECTION,
    T.SUBJECT,
    S.[GROUP],
    
    -- FIXED: Count distinct Roll Numbers to avoid join-multiplication
    COUNT(DISTINCT M.ROLLNO) AS APPEARED,
    
    COUNT(DISTINCT CASE WHEN UPPER(ISNULL(M.Remarks,'')) = 'A' THEN M.ROLLNO END) AS ABSENT,

    COUNT(DISTINCT CASE WHEN UPPER(ISNULL(M.Remarks,'')) <> 'A' 
              AND ISNUMERIC(M.[%]) = 1 
              AND CAST(M.[%] AS DECIMAL(10,2)) >= 40 THEN M.ROLLNO END) AS PASS,

    -- GRADE COUNTS (Using DISTINCT to ensure counts match student total of 33)
    COUNT(DISTINCT CASE WHEN UPPER(ISNULL(M.Remarks,'')) <> 'A' AND M.GRADE = 'A+' THEN M.ROLLNO END) AS [A+],
    COUNT(DISTINCT CASE WHEN UPPER(ISNULL(M.Remarks,'')) <> 'A' AND M.GRADE = 'A'  THEN M.ROLLNO END) AS [A],
    COUNT(DISTINCT CASE WHEN UPPER(ISNULL(M.Remarks,'')) <> 'A' AND M.GRADE = 'B'  THEN M.ROLLNO END) AS [B],
    COUNT(DISTINCT CASE WHEN UPPER(ISNULL(M.Remarks,'')) <> 'A' AND M.GRADE = 'C'  THEN M.ROLLNO END) AS [C],
    COUNT(DISTINCT CASE WHEN UPPER(ISNULL(M.Remarks,'')) <> 'A' AND M.GRADE = 'D'  THEN M.ROLLNO END) AS [D],
    COUNT(DISTINCT CASE WHEN UPPER(ISNULL(M.Remarks,'')) <> 'A' AND M.GRADE = 'E'  THEN M.ROLLNO END) AS [E],
    COUNT(DISTINCT CASE WHEN UPPER(ISNULL(M.Remarks,'')) <> 'A' AND M.GRADE = 'F'  THEN M.ROLLNO END) AS [F],

    -- AVERAGES (Calculated using the specific subject marks)
    CAST((SUM(CASE WHEN UPPER(ISNULL(M.Remarks,'')) <> 'A' THEN CAST(ISNULL(M.OBTAINED,0) AS DECIMAL(10,2)) ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN UPPER(ISNULL(M.Remarks,'')) <> 'A' THEN CAST(ISNULL(M.TOTAL,0) AS DECIMAL(10,2)) ELSE 0 END), 0)) * 100 
    AS DECIMAL(10,2)) AS [CLASS%],

    CAST(AVG(CASE WHEN UPPER(ISNULL(M.Remarks,'')) <> 'A' THEN CAST(M.OBTAINED AS DECIMAL(10,2)) END) 
    AS DECIMAL(10,2)) AS CLASS_AVG,

    -- PERCENTAGE BINS (Fixed with DISTINCT)
    COUNT(DISTINCT CASE WHEN UPPER(ISNULL(M.Remarks,'')) <> 'A' AND ISNUMERIC(M.[%]) = 1 AND CAST(M.[%] AS DECIMAL(10,2)) < 70 THEN M.ROLLNO END) AS [BELOW 70%],
    COUNT(DISTINCT CASE WHEN UPPER(ISNULL(M.Remarks,'')) <> 'A' AND ISNUMERIC(M.[%]) = 1 AND CAST(M.[%] AS DECIMAL(10,2)) >= 70 THEN M.ROLLNO END) AS [ABOVE 70%]

FROM TEACHERS_INTERNAL_EXAM T
INNER JOIN SUBJECT_GORUP_YEAR_MARKS_26 G
    ON T.SUBJECT = G.SUBJECT 
    AND T.CLASS = G.CLASS 
    AND T.YEAR = G.YEAR
INNER JOIN STUDENTS_ROLL_INTERNAL_EXAM S 
    ON T.CLASS = S.CLASS 
    AND T.SECTION = S.SECTION 
    AND T.SCHOOL = S.SCHOOL 
    AND T.YEAR = S.YEAR
    AND S.[GROUP] = G.[GROUP]
    AND T.EXAM = S.EXAM 
LEFT JOIN Marks_Internal M 
    ON S.ROLLNO = M.ROLLNO 
    AND T.SUBJECT = M.SUBJECT 
    AND T.EXAM = M.EXAMTYPE
    AND T.YEAR = M.YEAR

GROUP BY 
    T.ID, T.SCHOOL, T.EXAM, T.EID, T.NAME, T.YEAR, T.CLASS, T.SECTION, T.SUBJECT, S.[GROUP];

GO

-- View: [dbo].[INTERNAL_STUDENT_RESULT_CARD_VIEW] (Object ID: 1398296041)
-- Created: 2025-12-17T23:19:28.117 | Modified: 2026-03-19T22:21:54.547
CREATE VIEW [dbo].[INTERNAL_STUDENT_RESULT_CARD_VIEW] AS
SELECT 
    S.SCHOOL, S.ROLLNO, S.SMSNO, S.STUDENT AS [STUDENT NAME], S.FATHER AS [FATHER NAME],
    S.CLASS, S.SECTION, S.YEAR, S.[GROUP], S.CATEGORY, S.BOARDROLLNO, S.HOUSE,
    S.EXAM, 
    M.SUBJECT, M.TOTAL, M.OBTAINED, M.[%] AS PERCENTAGE,
    
    -- --- NEW DYNAMIC GRADING LOGIC ---
    CASE 
        -- Group 1: Middle School (6, 7, 8)
        WHEN S.CLASS IN ('6', '7', '8', '06', '07', '08') THEN
            CASE 
                WHEN M.[%] >= 90 THEN 'A+'
                WHEN M.[%] >= 80 THEN 'A'
                WHEN M.[%] >= 70 THEN 'B'
                WHEN M.[%] >= 60 THEN 'C'
                WHEN M.[%] >= 50 THEN 'D'
                WHEN M.[%] >= 40 THEN 'E'
                ELSE 'F'
            END
        -- Group 2: Senior/Inter (9, 10, 11, 12)
        WHEN S.CLASS IN ('9', '10', '11', '12', '09') THEN
            CASE 
                WHEN M.[%] >= 90 THEN 'A+'
                WHEN M.[%] >= 80 THEN 'A'
                WHEN M.[%] >= 70 THEN 'B'
                WHEN M.[%] >= 60 THEN 'C'
                WHEN M.[%] >= 50 THEN 'D'
                WHEN M.[%] >= 33 THEN 'E'
                ELSE 'F'
            END
        ELSE 'F'
    END AS GRADE,

    -- --- NEW DYNAMIC PASS/FAIL STATUS ---
    CASE 
        WHEN S.CLASS IN ('6', '7', '8', '06', '07', '08') THEN
            CASE WHEN M.[%] >= 40 THEN 'PASS' ELSE 'FAIL' END
        ELSE
            CASE WHEN M.[%] >= 33 THEN 'PASS' ELSE 'FAIL' END
    END AS STATUS,

    ISNULL(M.Remarks, 'NOT CONDUCTED/ABSENT') AS REMARKS
FROM STUDENTS_ROLL_INTERNAL_EXAM S
LEFT JOIN Marks_Internal M 
    ON S.ROLLNO = M.ROLLNO 
    AND S.EXAM = M.EXAMTYPE 
    AND S.YEAR = M.YEAR;

GO

-- View: [dbo].[INTERNAL_STUDENT_SUMMARY_RANKS] (Object ID: 1414296098)
-- Created: 2025-12-17T23:28:47.297 | Modified: 2026-01-27T05:52:52.657
CREATE VIEW [dbo].[INTERNAL_STUDENT_SUMMARY_RANKS] AS
WITH StudentBaseData AS (
    SELECT 
        S.SCHOOL, 
        S.ROLLNO, 
        S.CLASS, 
        S.SECTION, 
        S.HOUSE,
        S.YEAR, 
        S.EXAM, -- Using S.EXAM as the master reference
        M.TOTAL,
        M.OBTAINED
    FROM STUDENTS_ROLL_INTERNAL_EXAM S
    INNER JOIN Marks_Internal M ON S.ROLLNO = M.ROLLNO 
                               AND S.CLASS = M.CLASS 
                               AND S.YEAR = M.YEAR
                               AND S.EXAM = M.EXAMTYPE -- CRITICAL FIX: Match the exam types
),
StudentTotals AS (
    SELECT 
        SCHOOL, ROLLNO, CLASS, SECTION, HOUSE, YEAR, EXAM as EXAMTYPE,
        SUM(CAST(TOTAL AS FLOAT)) as GrandTotal,
        SUM(CAST(OBTAINED AS FLOAT)) as GrandObtained
    FROM StudentBaseData
    GROUP BY SCHOOL, ROLLNO, CLASS, SECTION, HOUSE, YEAR, EXAM
),
CalculatedRanks AS (
    SELECT *,
        CASE WHEN GrandTotal > 0 THEN (GrandObtained / GrandTotal) * 100 ELSE 0 END as OverallPercentage,
        
        -- 1. POSITION IN SECTION (Filtered by specific Exam)
        RANK() OVER (PARTITION BY SCHOOL, CLASS, SECTION, YEAR, EXAMTYPE ORDER BY GrandObtained DESC) as PositionInSection,
        
        -- 2. POSITION IN CLASS (Filtered by specific Exam)
        RANK() OVER (PARTITION BY SCHOOL, CLASS, YEAR, EXAMTYPE ORDER BY GrandObtained DESC) as PositionInClass,
        
        -- 3. POSITION IN HOUSE (Filtered by specific Exam)
        RANK() OVER (PARTITION BY SCHOOL, HOUSE, YEAR, EXAMTYPE ORDER BY GrandObtained DESC) as PositionInHouse,
        
        -- 4. POSITION IN SCHOOL (Filtered by specific Exam)
        RANK() OVER (PARTITION BY SCHOOL, YEAR, EXAMTYPE ORDER BY GrandObtained DESC) as PositionInSchool
    FROM StudentTotals
)
SELECT * FROM CalculatedRanks;

GO

-- View: [dbo].[Incorrect_Rollno_Check] (Object ID: 2046630334)
-- Created: 2025-06-15T09:06:46.720 | Modified: 2025-06-15T09:06:46.720
CREATE VIEW [dbo].[Incorrect_Rollno_Check] AS
SELECT 
  sr.SCHOOL,
  sr.CLASS,
  sr.YEAR,
  sr.SMSNO,
  sr.ROLLNO,

  -- Construct expected roll number and cast as INT
  CAST(CONCAT(
    CASE sr.SCHOOL
      WHEN 'CTNB' THEN '1' WHEN 'CTNG' THEN '2'
      WHEN 'RYKB' THEN '3' WHEN 'RYKG' THEN '4'
      WHEN 'RJNB' THEN '5' WHEN 'RJNG' THEN '6'
      WHEN 'HSPB' THEN '7' WHEN 'HSPG' THEN '8'
      WHEN 'VEHB' THEN '9' WHEN 'VEHG' THEN '10'
      WHEN 'DGKB' THEN '11' WHEN 'DGKG' THEN '12'
      WHEN 'MNWB' THEN '13' WHEN 'MNWG' THEN '14'
      WHEN 'ATKB' THEN '15' WHEN 'ATKG' THEN '16'
    END,
    RIGHT('00' + CAST(sr.YEAR AS VARCHAR), 2),
    RIGHT('00' + CAST(sr.CLASS AS VARCHAR), 2),
    RIGHT('0000' + CAST(sr.SMSNO AS VARCHAR), 4)
  ) AS BIGINT) AS Expected_ROLLNO,

  -- Difference (should be 0 if correct)
  CAST(CONCAT(
    CASE sr.SCHOOL
      WHEN 'CTNB' THEN '1' WHEN 'CTNG' THEN '2'
      WHEN 'RYKB' THEN '3' WHEN 'RYKG' THEN '4'
      WHEN 'RJNB' THEN '5' WHEN 'RJNG' THEN '6'
      WHEN 'HSPB' THEN '7' WHEN 'HSPG' THEN '8'
      WHEN 'VEHB' THEN '9' WHEN 'VEHG' THEN '10'
      WHEN 'DGKB' THEN '11' WHEN 'DGKG' THEN '12'
      WHEN 'MNWB' THEN '13' WHEN 'MNWG' THEN '14'
      WHEN 'ATKB' THEN '15' WHEN 'ATKG' THEN '16'
    END,
    RIGHT('00' + CAST(sr.YEAR AS VARCHAR), 2),
    RIGHT('00' + CAST(sr.CLASS AS VARCHAR), 2),
    RIGHT('0000' + CAST(sr.SMSNO AS VARCHAR), 4)
  ) AS BIGINT) - sr.ROLLNO AS Incorrect_Rollno

FROM STUDENTS_ROLL sr
WHERE sr.CLASS IN (6, 7, 8)
  AND sr.ROLLNO IS NOT NULL;

GO

-- View: [dbo].[MTT] (Object ID: 2126630619)
-- Created: 2025-06-15T11:26:03.013 | Modified: 2025-06-15T11:45:04.040
CREATE VIEW [dbo].[MTT] AS
SELECT q1.*
FROM QUERY1 AS q1
WHERE q1.CATEGROY = 'ALL'
  AND NOT EXISTS (
      SELECT 1
      FROM TEAHCERS AS t
      WHERE q1.SCHOOL = t.SCHOOL
        AND q1.SUBJECT = t.SUBJECT
        AND q1.CLASS = t.CLASS
        AND q1.SECTION = t.SECTION
        AND q1.YEAR = t.YEAR
  );

GO

-- View: [dbo].[Query1] (Object ID: 2094630505)
-- Created: 2025-06-15T11:21:14.133 | Modified: 2025-06-15T11:21:14.133
CREATE VIEW [dbo].[Query1] AS
SELECT 
    SR.SCHOOL, 
    M.EXAMTYPE, 
    M.SUBJECT, 
    SR.CLASS, 
    SR.SECTION, 
    SR.Year, 
    SR.CATEGROY, 

    COUNT(*) AS [STRENGTH],

    COUNT(CASE WHEN M.[%] BETWEEN 90 AND 100 THEN 1 END) AS [Count_90_100],
    COUNT(CASE WHEN M.[%] >= 80 AND M.[%] < 90 THEN 1 END) AS [Count_80_90],
    COUNT(CASE WHEN M.[%] >= 70 AND M.[%] < 80 THEN 1 END) AS [Count_70_80],
    COUNT(CASE WHEN M.[%] >= 60 AND M.[%] < 70 THEN 1 END) AS [Count_60_70],
    COUNT(CASE WHEN M.[%] >= 50 AND M.[%] < 60 THEN 1 END) AS [Count_50_60],
    COUNT(CASE WHEN M.[%] >= 40 AND M.[%] < 50 THEN 1 END) AS [Count_40_50],
    COUNT(CASE WHEN M.[%] >= 0 AND M.[%] < 40 THEN 1 END) AS [Count_0_39],

    COUNT(*) AS [APPEARED],
    COUNT(CASE 
              WHEN (SR.CLASS IN (9,10,11,12) AND M.[%] >= 33) OR 
                   (SR.CLASS IN (6,7,8) AND M.[%] >= 40) THEN 1 
         END) AS [PASSED],

    ROUND(CAST(COUNT(CASE 
              WHEN (SR.CLASS IN (9,10,11,12) AND M.[%] >= 33) OR 
                   (SR.CLASS IN (6,7,8) AND M.[%] >= 40) THEN 1 
         END) * 100.0 / COUNT(*) AS DECIMAL(5,2)), 2) AS [PASS%],

    ROUND(AVG(M.[%]), 2) AS [CLASS AVG]

FROM 
    STUDENTS_ROLL SR
    INNER JOIN MARKS M ON SR.ROLLNO = M.ROLLNO 
                       AND SR.CLASS = M.CLASS 
                       AND SR.YEAR = M.YEAR

GROUP BY 
    SR.SCHOOL, 
    M.EXAMTYPE, 
    M.SUBJECT, 
    SR.CLASS, 
    SR.SECTION, 
    SR.Year, 
    SR.CATEGROY

UNION ALL

SELECT 
    CA.SCHOOL, 
    CA.EXAMTYPE, 
    CA.SUBJECT, 
    CA.CLASS, 
    CA.SECTION, 
    CA.Year, 
    'ALL' AS CATEGROY,  

    SUM(CA.STRENGTH) AS [STRENGTH],

    SUM(CA.[Count_90_100]) AS [Count_90_100],
    SUM(CA.[Count_80_90]) AS [Count_80_90],
    SUM(CA.[Count_70_80]) AS [Count_70_80],
    SUM(CA.[Count_60_70]) AS [Count_60_70],
    SUM(CA.[Count_50_60]) AS [Count_50_60],
    SUM(CA.[Count_40_50]) AS [Count_40_50],
    SUM(CA.[Count_0_39]) AS [Count_0_39],

    SUM(CA.TotalCount) AS [APPEARED],
    SUM(CA.PASSED) AS [PASSED],
    ROUND(SUM(CA.PASSED) * 100.0 / SUM(CA.TotalCount), 2) AS [PASS%],

    ROUND(SUM(CA.[AvgOf%] * CA.STRENGTH) / SUM(CA.STRENGTH), 2) AS [CLASS AVG]

FROM (
    SELECT 
        SR.SCHOOL, 
        M.EXAMTYPE, 
        M.SUBJECT, 
        SR.CLASS, 
        SR.SECTION, 
        SR.Year, 
        SR.CATEGROY,

        COUNT(*) AS STRENGTH,
        COUNT(*) AS TotalCount,
        COUNT(CASE 
                  WHEN (SR.CLASS IN (9,10,11,12) AND M.[%] >= 33) OR 
                       (SR.CLASS IN (6,7,8) AND M.[%] >= 40) THEN 1 
             END) AS PASSED,

        SUM(M.OBTAINED) AS OBTAINED_SUM,
        SUM(M.TOTAL) AS TOTAL_SUM,
        AVG(M.[%]) AS [AvgOf%],

        COUNT(CASE WHEN M.[%] >= 90 THEN 1 END) AS [Count_90_100],
        COUNT(CASE WHEN M.[%] >= 80 AND M.[%] < 90 THEN 1 END) AS [Count_80_90],
        COUNT(CASE WHEN M.[%] >= 70 AND M.[%] < 80 THEN 1 END) AS [Count_70_80],
        COUNT(CASE WHEN M.[%] >= 60 AND M.[%] < 70 THEN 1 END) AS [Count_60_70],
        COUNT(CASE WHEN M.[%] >= 50 AND M.[%] < 60 THEN 1 END) AS [Count_50_60],
        COUNT(CASE WHEN M.[%] >= 40 AND M.[%] < 50 THEN 1 END) AS [Count_40_50],
        COUNT(CASE WHEN M.[%] >= 0 AND M.[%] < 40 THEN 1 END) AS [Count_0_39]

    FROM STUDENTS_ROLL SR
    INNER JOIN MARKS M ON SR.ROLLNO = M.ROLLNO
    GROUP BY SR.SCHOOL, M.EXAMTYPE, M.SUBJECT, SR.CLASS, SR.SECTION, SR.Year, SR.CATEGROY
) AS CA

GROUP BY 
    CA.SCHOOL, 
    CA.EXAMTYPE, 
    CA.SUBJECT, 
    CA.CLASS, 
    CA.SECTION, 
    CA.Year;

GO

-- View: [dbo].[Query1_Prac] (Object ID: 1751677288)
-- Created: 2025-07-26T10:32:09.417 | Modified: 2025-07-26T10:32:09.417
CREATE VIEW [dbo].[Query1_Prac] AS
SELECT 
    SR.SCHOOL, 
    V.EXAMTYPE, 
    V.SUBJECT, 
    SR.CLASS, 
    SR.SECTION, 
    SR.Year, 
    SR.CATEGROY, 

    COUNT(*) AS [STRENGTH],

    COUNT(CASE WHEN V.[%] BETWEEN 90 AND 100 THEN 1 END) AS [Count_90_100],
    COUNT(CASE WHEN V.[%] >= 80 AND V.[%] < 90 THEN 1 END) AS [Count_80_90],
    COUNT(CASE WHEN V.[%] >= 70 AND V.[%] < 80 THEN 1 END) AS [Count_70_80],
    COUNT(CASE WHEN V.[%] >= 60 AND V.[%] < 70 THEN 1 END) AS [Count_60_70],
    COUNT(CASE WHEN V.[%] >= 50 AND V.[%] < 60 THEN 1 END) AS [Count_50_60],
    COUNT(CASE WHEN V.[%] >= 40 AND V.[%] < 50 THEN 1 END) AS [Count_40_50],
    COUNT(CASE WHEN V.[%] >= 0 AND V.[%] < 40 THEN 1 END) AS [Count_0_39],

    COUNT(*) AS [APPEARED],
    COUNT(CASE 
        WHEN (SR.CLASS IN (9,10,11,12) AND V.[%] >= 33) OR 
             (SR.CLASS IN (6,7,8) AND V.[%] >= 40) THEN 1 
    END) AS [PASSED],

    ROUND(CAST(COUNT(CASE 
        WHEN (SR.CLASS IN (9,10,11,12) AND V.[%] >= 33) OR 
             (SR.CLASS IN (6,7,8) AND V.[%] >= 40) THEN 1 
    END) * 100.0 / COUNT(*) AS DECIMAL(5,2)), 2) AS [PASS%],

    ROUND(AVG(V.[%]), 2) AS [CLASS AVG]

FROM 
    STUDENTS_ROLL SR
    INNER JOIN PRAC V ON SR.ROLLNO = V.ROLLNO 
                        AND SR.CLASS = V.CLASS 
                        AND SR.YEAR = V.YEAR

GROUP BY 
    SR.SCHOOL, 
    V.EXAMTYPE, 
    V.SUBJECT, 
    SR.CLASS, 
    SR.SECTION, 
    SR.Year, 
    SR.CATEGROY

UNION ALL

SELECT 
    CA.SCHOOL, 
    CA.EXAMTYPE, 
    CA.SUBJECT, 
    CA.CLASS, 
    CA.SECTION, 
    CA.Year, 
    'ALL' AS CATEGROY,  

    SUM(CA.STRENGTH) AS [STRENGTH],

    SUM(CA.[Count_90_100]) AS [Count_90_100],
    SUM(CA.[Count_80_90]) AS [Count_80_90],
    SUM(CA.[Count_70_80]) AS [Count_70_80],
    SUM(CA.[Count_60_70]) AS [Count_60_70],
    SUM(CA.[Count_50_60]) AS [Count_50_60],
    SUM(CA.[Count_40_50]) AS [Count_40_50],
    SUM(CA.[Count_0_39]) AS [Count_0_39],

    SUM(CA.TotalCount) AS [APPEARED],
    SUM(CA.PASSED) AS [PASSED],
    ROUND(SUM(CA.PASSED) * 100.0 / SUM(CA.TotalCount), 2) AS [PASS%],

    ROUND(SUM(CA.[AvgOf%] * CA.STRENGTH) / SUM(CA.STRENGTH), 2) AS [CLASS AVG]

FROM (
    SELECT 
        SR.SCHOOL, 
        V.EXAMTYPE, 
        V.SUBJECT, 
        SR.CLASS, 
        SR.SECTION, 
        SR.Year, 
        SR.CATEGROY,

        COUNT(*) AS STRENGTH,
        COUNT(*) AS TotalCount,
        COUNT(CASE 
              WHEN (SR.CLASS IN (9,10,11,12) AND V.[%] >= 33) OR 
                   (SR.CLASS IN (6,7,8) AND V.[%] >= 40) THEN 1 
        END) AS PASSED,

        SUM(V.OBTAINED) AS OBTAINED_SUM,
        SUM(V.TOTAL) AS TOTAL_SUM,
        AVG(V.[%]) AS [AvgOf%],

        COUNT(CASE WHEN V.[%] >= 90 THEN 1 END) AS [Count_90_100],
        COUNT(CASE WHEN V.[%] >= 80 AND V.[%] < 90 THEN 1 END) AS [Count_80_90],
        COUNT(CASE WHEN V.[%] >= 70 AND V.[%] < 80 THEN 1 END) AS [Count_70_80],
        COUNT(CASE WHEN V.[%] >= 60 AND V.[%] < 70 THEN 1 END) AS [Count_60_70],
        COUNT(CASE WHEN V.[%] >= 50 AND V.[%] < 60 THEN 1 END) AS [Count_50_60],
        COUNT(CASE WHEN V.[%] >= 40 AND V.[%] < 50 THEN 1 END) AS [Count_40_50],
        COUNT(CASE WHEN V.[%] >= 0 AND V.[%] < 40 THEN 1 END) AS [Count_0_39]

    FROM STUDENTS_ROLL SR
    INNER JOIN PRAC V ON SR.ROLLNO = V.ROLLNO
                         AND SR.CLASS = V.CLASS
                         AND SR.YEAR = V.YEAR
    GROUP BY SR.SCHOOL, V.EXAMTYPE, V.SUBJECT, SR.CLASS, SR.SECTION, SR.Year, SR.CATEGROY
) AS CA

GROUP BY 
    CA.SCHOOL, 
    CA.EXAMTYPE, 
    CA.SUBJECT, 
    CA.CLASS, 
    CA.SECTION, 
    CA.Year;

GO

-- View: [dbo].[Query1_internal] (Object ID: 1293247662)
-- Created: 2025-11-13T13:59:24.403 | Modified: 2025-11-13T13:59:24.403
CREATE VIEW [dbo].[Query1_internal] AS
SELECT 
    SR.SCHOOL, 
    M.EXAMTYPE, 
    M.SUBJECT, 
    SR.CLASS, 
    SR.SECTION, 
    SR.Year, 
    SR.CATEGORY, 

    COUNT(*) AS [STRENGTH],

    COUNT(CASE WHEN CAST(M.[%] AS FLOAT) BETWEEN 90 AND 100 THEN 1 END) AS [Count_90_100],
    COUNT(CASE WHEN CAST(M.[%] AS FLOAT) >= 80 AND CAST(M.[%] AS FLOAT) < 90 THEN 1 END) AS [Count_80_90],
    COUNT(CASE WHEN CAST(M.[%] AS FLOAT) >= 70 AND CAST(M.[%] AS FLOAT) < 80 THEN 1 END) AS [Count_70_80],
    COUNT(CASE WHEN CAST(M.[%] AS FLOAT) >= 60 AND CAST(M.[%] AS FLOAT) < 70 THEN 1 END) AS [Count_60_70],
    COUNT(CASE WHEN CAST(M.[%] AS FLOAT) >= 50 AND CAST(M.[%] AS FLOAT) < 60 THEN 1 END) AS [Count_50_60],
    COUNT(CASE WHEN CAST(M.[%] AS FLOAT) >= 40 AND CAST(M.[%] AS FLOAT) < 50 THEN 1 END) AS [Count_40_50],
    COUNT(CASE WHEN CAST(M.[%] AS FLOAT) >= 0 AND CAST(M.[%] AS FLOAT) < 40 THEN 1 END) AS [Count_0_39],

    COUNT(*) AS [APPEARED],
    COUNT(CASE 
        WHEN (SR.CLASS IN (9,10,11,12) AND CAST(M.[%] AS FLOAT) >= 33) OR 
             (SR.CLASS IN (6,7,8) AND CAST(M.[%] AS FLOAT) >= 40) THEN 1 
         END) AS [PASSED],

    ROUND(CAST(COUNT(CASE 
          WHEN (SR.CLASS IN (9,10,11,12) AND CAST(M.[%] AS FLOAT) >= 33) OR 
               (SR.CLASS IN (6,7,8) AND CAST(M.[%] AS FLOAT) >= 40) THEN 1 
         END) * 100.0 / COUNT(*) AS DECIMAL(5,2)), 2) AS [PASS%],

    ROUND(AVG(CAST(M.[%] AS FLOAT)), 2) AS [CLASS AVG]

FROM 
    STUDENTS_ROLL_INTERNAL_EXAM SR
    INNER JOIN MARKS_INTERNAL M ON SR.ROLLNO = M.ROLLNO 
                                 AND SR.CLASS = M.CLASS 
                                 AND SR.YEAR = M.YEAR

GROUP BY 
    SR.SCHOOL, 
    M.EXAMTYPE, 
    M.SUBJECT, 
    SR.CLASS, 
    SR.SECTION, 
    SR.Year, 
    SR.CATEGORY

UNION ALL

SELECT 
    CA.SCHOOL, 
    CA.EXAMTYPE, 
    CA.SUBJECT, 
    CA.CLASS, 
    CA.SECTION, 
    CA.Year, 
    'ALL' AS CATEGORY,  

    SUM(CA.STRENGTH) AS [STRENGTH],

    SUM(CA.[Count_90_100]) AS [Count_90_100],
    SUM(CA.[Count_80_90]) AS [Count_80_90],
    SUM(CA.[Count_70_80]) AS [Count_70_80],
    SUM(CA.[Count_60_70]) AS [Count_60_70],
    SUM(CA.[Count_50_60]) AS [Count_50_60],
    SUM(CA.[Count_40_50]) AS [Count_40_50],
    SUM(CA.[Count_0_39]) AS [Count_0_39],

    SUM(CA.TotalCount) AS [APPEARED],
    SUM(CA.PASSED) AS [PASSED],
    ROUND(SUM(CA.PASSED) * 100.0 / SUM(CA.TotalCount), 2) AS [PASS%],

    ROUND(SUM(CA.[AvgOfPercent] * CA.STRENGTH) / SUM(CA.STRENGTH), 2) AS [CLASS AVG]

FROM (
    SELECT 
        SR.SCHOOL, 
        M.EXAMTYPE, 
        M.SUBJECT, 
        SR.CLASS, 
        SR.SECTION, 
        SR.Year, 
        SR.CATEGORY,

        COUNT(*) AS STRENGTH,
        COUNT(*) AS TotalCount,
        COUNT(CASE 
              WHEN (SR.CLASS IN (9,10,11,12) AND CAST(M.[%] AS FLOAT) >= 33) OR 
                   (SR.CLASS IN (6,7,8) AND CAST(M.[%] AS FLOAT) >= 40) THEN 1 
             END) AS PASSED,

        SUM(CAST(M.OBTAINED AS FLOAT)) AS OBTAINED_SUM,
        SUM(CAST(M.TOTAL AS FLOAT)) AS TOTAL_SUM,
        AVG(CAST(M.[%] AS FLOAT)) AS [AvgOfPercent],

        COUNT(CASE WHEN CAST(M.[%] AS FLOAT) >= 90 THEN 1 END) AS [Count_90_100],
        COUNT(CASE WHEN CAST(M.[%] AS FLOAT) >= 80 AND CAST(M.[%] AS FLOAT) < 90 THEN 1 END) AS [Count_80_90],
        COUNT(CASE WHEN CAST(M.[%] AS FLOAT) >= 70 AND CAST(M.[%] AS FLOAT) < 80 THEN 1 END) AS [Count_70_80],
        COUNT(CASE WHEN CAST(M.[%] AS FLOAT) >= 60 AND CAST(M.[%] AS FLOAT) < 70 THEN 1 END) AS [Count_60_70],
        COUNT(CASE WHEN CAST(M.[%] AS FLOAT) >= 50 AND CAST(M.[%] AS FLOAT) < 60 THEN 1 END) AS [Count_50_60],
        COUNT(CASE WHEN CAST(M.[%] AS FLOAT) >= 40 AND CAST(M.[%] AS FLOAT) < 50 THEN 1 END) AS [Count_40_50],
        COUNT(CASE WHEN CAST(M.[%] AS FLOAT) >= 0 AND CAST(M.[%] AS FLOAT) < 40 THEN 1 END) AS [Count_0_39]

    FROM STUDENTS_ROLL_INTERNAL_EXAM SR
    INNER JOIN MARKS_INTERNAL M ON SR.ROLLNO = M.ROLLNO
    GROUP BY SR.SCHOOL, M.EXAMTYPE, M.SUBJECT, SR.CLASS, SR.SECTION, SR.Year, SR.CATEGORY
) AS CA

GROUP BY 
    CA.SCHOOL, 
    CA.EXAMTYPE, 
    CA.SUBJECT, 
    CA.CLASS, 
    CA.SECTION, 
    CA.Year;

GO

-- View: [dbo].[Query1_theory] (Object ID: 1735677231)
-- Created: 2025-07-26T10:30:20.803 | Modified: 2025-07-26T10:30:20.803
CREATE VIEW [dbo].[Query1_theory] AS
SELECT 
    SR.SCHOOL, 
    V.EXAMTYPE, 
    V.SUBJECT, 
    SR.CLASS, 
    SR.SECTION, 
    SR.Year, 
    SR.CATEGROY, 

    COUNT(*) AS [STRENGTH],

    COUNT(CASE WHEN V.[%] BETWEEN 90 AND 100 THEN 1 END) AS [Count_90_100],
    COUNT(CASE WHEN V.[%] >= 80 AND V.[%] < 90 THEN 1 END) AS [Count_80_90],
    COUNT(CASE WHEN V.[%] >= 70 AND V.[%] < 80 THEN 1 END) AS [Count_70_80],
    COUNT(CASE WHEN V.[%] >= 60 AND V.[%] < 70 THEN 1 END) AS [Count_60_70],
    COUNT(CASE WHEN V.[%] >= 50 AND V.[%] < 60 THEN 1 END) AS [Count_50_60],
    COUNT(CASE WHEN V.[%] >= 40 AND V.[%] < 50 THEN 1 END) AS [Count_40_50],
    COUNT(CASE WHEN V.[%] >= 0 AND V.[%] < 40 THEN 1 END) AS [Count_0_39],

    COUNT(*) AS [APPEARED],
    COUNT(CASE 
        WHEN (SR.CLASS IN (9,10,11,12) AND V.[%] >= 33) OR 
             (SR.CLASS IN (6,7,8) AND V.[%] >= 40) THEN 1 
    END) AS [PASSED],

    ROUND(CAST(COUNT(CASE 
        WHEN (SR.CLASS IN (9,10,11,12) AND V.[%] >= 33) OR 
             (SR.CLASS IN (6,7,8) AND V.[%] >= 40) THEN 1 
    END) * 100.0 / COUNT(*) AS DECIMAL(5,2)), 2) AS [PASS%],

    ROUND(AVG(V.[%]), 2) AS [CLASS AVG]

FROM 
    STUDENTS_ROLL SR
    INNER JOIN vTheory V ON SR.ROLLNO = V.ROLLNO 
                        AND SR.CLASS = V.CLASS 
                        AND SR.YEAR = V.YEAR

GROUP BY 
    SR.SCHOOL, 
    V.EXAMTYPE, 
    V.SUBJECT, 
    SR.CLASS, 
    SR.SECTION, 
    SR.Year, 
    SR.CATEGROY

UNION ALL

SELECT 
    CA.SCHOOL, 
    CA.EXAMTYPE, 
    CA.SUBJECT, 
    CA.CLASS, 
    CA.SECTION, 
    CA.Year, 
    'ALL' AS CATEGROY,  

    SUM(CA.STRENGTH) AS [STRENGTH],

    SUM(CA.[Count_90_100]) AS [Count_90_100],
    SUM(CA.[Count_80_90]) AS [Count_80_90],
    SUM(CA.[Count_70_80]) AS [Count_70_80],
    SUM(CA.[Count_60_70]) AS [Count_60_70],
    SUM(CA.[Count_50_60]) AS [Count_50_60],
    SUM(CA.[Count_40_50]) AS [Count_40_50],
    SUM(CA.[Count_0_39]) AS [Count_0_39],

    SUM(CA.TotalCount) AS [APPEARED],
    SUM(CA.PASSED) AS [PASSED],
    ROUND(SUM(CA.PASSED) * 100.0 / SUM(CA.TotalCount), 2) AS [PASS%],

    ROUND(SUM(CA.[AvgOf%] * CA.STRENGTH) / SUM(CA.STRENGTH), 2) AS [CLASS AVG]

FROM (
    SELECT 
        SR.SCHOOL, 
        V.EXAMTYPE, 
        V.SUBJECT, 
        SR.CLASS, 
        SR.SECTION, 
        SR.Year, 
        SR.CATEGROY,

        COUNT(*) AS STRENGTH,
        COUNT(*) AS TotalCount,
        COUNT(CASE 
              WHEN (SR.CLASS IN (9,10,11,12) AND V.[%] >= 33) OR 
                   (SR.CLASS IN (6,7,8) AND V.[%] >= 40) THEN 1 
        END) AS PASSED,

        SUM(V.OBTAINED) AS OBTAINED_SUM,
        SUM(V.TOTAL) AS TOTAL_SUM,
        AVG(V.[%]) AS [AvgOf%],

        COUNT(CASE WHEN V.[%] >= 90 THEN 1 END) AS [Count_90_100],
        COUNT(CASE WHEN V.[%] >= 80 AND V.[%] < 90 THEN 1 END) AS [Count_80_90],
        COUNT(CASE WHEN V.[%] >= 70 AND V.[%] < 80 THEN 1 END) AS [Count_70_80],
        COUNT(CASE WHEN V.[%] >= 60 AND V.[%] < 70 THEN 1 END) AS [Count_60_70],
        COUNT(CASE WHEN V.[%] >= 50 AND V.[%] < 60 THEN 1 END) AS [Count_50_60],
        COUNT(CASE WHEN V.[%] >= 40 AND V.[%] < 50 THEN 1 END) AS [Count_40_50],
        COUNT(CASE WHEN V.[%] >= 0 AND V.[%] < 40 THEN 1 END) AS [Count_0_39]

    FROM STUDENTS_ROLL SR
    INNER JOIN vTheory V ON SR.ROLLNO = V.ROLLNO
                         AND SR.CLASS = V.CLASS
                         AND SR.YEAR = V.YEAR
    GROUP BY SR.SCHOOL, V.EXAMTYPE, V.SUBJECT, SR.CLASS, SR.SECTION, SR.Year, SR.CATEGROY
) AS CA

GROUP BY 
    CA.SCHOOL, 
    CA.EXAMTYPE, 
    CA.SUBJECT, 
    CA.CLASS, 
    CA.SECTION, 
    CA.Year;

GO

-- View: [dbo].[SEC_CAT_MISSING_COUNT] (Object ID: 1163151189)
-- Created: 2025-06-29T11:39:00.863 | Modified: 2025-06-29T11:40:21.120
CREATE VIEW [dbo].[SEC_CAT_MISSING_COUNT] AS
WITH MissingResults AS (
    SELECT
        SCHOOL,
        CLASS,
        YEAR,
        ROLLNO
    FROM vw_MissingResultsWithStatus
    WHERE CLASS IN (6, 7, 8, 9, 10, 11, 12)
      AND Status = 'Missing'
    GROUP BY
        SCHOOL,
        CLASS,
        YEAR,
        ROLLNO
),

Base AS (
    SELECT
        sr.SCHOOL,
        sr.CLASS,
        sr.YEAR,
        sr.SECTION,
        sr.CATEGROY,
        sr.FATHER,
        sr.[GROUP],
        sr.SMSNO,
        sr.ROLLNO,
        ISNULL(vw.Incorrect_Rollno, 0) AS Incorrect_Rollno
    FROM STUDENTS_ROLL AS sr
    LEFT JOIN Incorrect_Rollno_Check AS vw
        ON sr.SCHOOL = vw.SCHOOL
       AND sr.CLASS = vw.CLASS
       AND sr.YEAR = vw.YEAR
       AND sr.SMSNO = vw.SMSNO
    WHERE sr.CLASS IN (6, 7, 8, 9, 10, 11, 12)
),

-- Identify distinct duplicated SMSNOs in Base
DuplicateSMSNOs AS (
    SELECT DISTINCT
        b.SCHOOL,
        b.CLASS,
        b.YEAR,
        b.SMSNO
    FROM Base AS b
    INNER JOIN vw_Duplicate_SMSNO AS d
        ON b.SCHOOL = d.SCHOOL
       AND b.CLASS = d.CLASS
       AND b.YEAR = d.YEAR
       AND b.SMSNO = d.SMSNO
),

-- Identify distinct duplicated ROLLNOs in Base
DuplicateROLLNOs AS (
    SELECT DISTINCT
        b.SCHOOL,
        b.CLASS,
        b.YEAR,
        b.ROLLNO
    FROM Base AS b
    INNER JOIN vw_Duplicate_ROLLNO AS r
        ON b.SCHOOL = r.SCHOOL
       AND b.CLASS = r.CLASS
       AND b.YEAR = r.YEAR
       AND b.ROLLNO = r.ROLLNO
),

Combined AS (
    SELECT
        b.*,
        -- Other quality flags
        CASE
            WHEN b.ROLLNO IS NULL OR LTRIM(RTRIM(CAST(b.ROLLNO AS VARCHAR))) = '' THEN 1
            ELSE 0
        END AS Missing_Rollno,
        CASE
            WHEN CAST(b.SMSNO AS VARCHAR) = CAST(b.ROLLNO AS VARCHAR) THEN 1
            ELSE 0
        END AS Same_SMSNO_Rollno
    FROM Base AS b
),

FinalAgg AS (
    SELECT
        c.SCHOOL,
        c.CLASS,
        c.YEAR,
        SUM(CASE WHEN c.SECTION IS NULL OR c.SECTION = '' THEN 1 ELSE 0 END) AS Section_Missing_Count,
        SUM(CASE WHEN c.CATEGROY IS NULL OR c.CATEGROY = '' THEN 1 ELSE 0 END) AS Categroy_Missing_Count,
        SUM(CASE WHEN c.FATHER IS NULL OR c.FATHER = '' THEN 1 ELSE 0 END) AS Father_Missing_Count,
        SUM(CASE WHEN c.CATEGROY NOT IN ('B','DS','S') THEN 1 ELSE 0 END) AS Invalid_Categroy_Count,
        SUM(CASE
                WHEN LTRIM(RTRIM(c.[GROUP])) NOT IN ('GENERAL SCIENCE','PRE-MEDICAL','PRE-ENGINEERING')
                THEN 1 ELSE 0
            END) AS Invalid_Group_Count,
        SUM(CASE WHEN c.SMSNO IS NULL THEN 1 ELSE 0 END) AS SMS_Missing_Count,
        COUNT(DISTINCT s.SMSNO) AS Duplicate_SMSNO_Count,
        COUNT(DISTINCT r.ROLLNO) AS Duplicate_Rollno_Count,
        SUM(CASE WHEN c.Incorrect_Rollno <> 0 THEN 1 ELSE 0 END) AS Incorrect_Rollno_Count,
        SUM(Missing_Rollno) AS Missing_Rollno_Count,
        SUM(Same_SMSNO_Rollno) AS Same_SMSNO_Rollno_Count
    FROM Combined AS c
    LEFT JOIN DuplicateSMSNOs AS s
        ON c.SCHOOL = s.SCHOOL
       AND c.CLASS = s.CLASS
       AND c.YEAR = s.YEAR
       AND c.SMSNO = s.SMSNO
    LEFT JOIN DuplicateROLLNOs AS r
        ON c.SCHOOL = r.SCHOOL
       AND c.CLASS = r.CLASS
       AND c.YEAR = r.YEAR
       AND c.ROLLNO = r.ROLLNO
    GROUP BY
        c.SCHOOL,
        c.CLASS,
        c.YEAR
),

ResultMissing AS (
    SELECT
        SCHOOL,
        CLASS,
        YEAR,
        COUNT(DISTINCT ROLLNO) AS RSLT_MISSING
    FROM MissingResults
    GROUP BY
        SCHOOL,
        CLASS,
        YEAR
)

SELECT
    fa.SCHOOL,
    fa.CLASS,
    fa.YEAR,
    fa.Section_Missing_Count,
    fa.Categroy_Missing_Count,
    fa.Father_Missing_Count,
    fa.Invalid_Categroy_Count,
    fa.Invalid_Group_Count,
    fa.SMS_Missing_Count,
    ISNULL(rm.RSLT_MISSING, 0) AS RSLT_MISSING,
    fa.Duplicate_SMSNO_Count,
    fa.Duplicate_Rollno_Count,
    fa.Incorrect_Rollno_Count,
    fa.Missing_Rollno_Count,
    fa.Same_SMSNO_Rollno_Count
FROM FinalAgg AS fa
LEFT JOIN ResultMissing AS rm
    ON fa.SCHOOL = rm.SCHOOL
   AND fa.CLASS = rm.CLASS
   AND fa.YEAR = rm.YEAR;

GO

-- View: [dbo].[SEC_CAT_MISSING_COUNT2] (Object ID: 939150391)
-- Created: 2025-06-27T17:26:47.340 | Modified: 2025-06-27T17:26:47.340
CREATE VIEW [dbo].[SEC_CAT_MISSING_COUNT2] AS
WITH MissingResults AS (
  SELECT
    SCHOOL,
    CLASS,
    YEAR,
    ROLLNO
  FROM vw_MissingResultsWithStatus
  WHERE CLASS IN (6, 7, 8, 9, 10, 11, 12)
    AND Status = 'Missing'
  GROUP BY
    SCHOOL,
    CLASS,
    YEAR,
    ROLLNO
),

Base AS (
  SELECT
    sr.SCHOOL,
    sr.CLASS,
    sr.YEAR,
    sr.SECTION,
    sr.CATEGROY,
    sr.FATHER,
    sr.[GROUP],
    sr.SMSNO,
    sr.ROLLNO,
    ISNULL(vw.Incorrect_Rollno, 0) AS Incorrect_Rollno
  FROM STUDENTS_ROLL AS sr
  LEFT JOIN Incorrect_Rollno_Check AS vw
    ON sr.SCHOOL = vw.SCHOOL
   AND sr.CLASS = vw.CLASS
   AND sr.YEAR = vw.YEAR
   AND sr.SMSNO = vw.SMSNO
  WHERE sr.CLASS IN (6, 7, 8, 9, 10, 11, 12)
),

Combined AS (
  SELECT
    b.*,
    -- Use vw_Duplicate_SMSNO to flag duplicates
    CASE WHEN d.SMSNO IS NOT NULL THEN 1 ELSE 0 END AS IsDuplicate_SMSNO,

    -- Rollno duplicates still calculated in-place
    COUNT(*) OVER (
      PARTITION BY b.SCHOOL, b.YEAR, b.ROLLNO
    ) AS cnt_rollno_school_year,

    -- Other flags
    CASE
      WHEN b.ROLLNO IS NULL OR LTRIM(RTRIM(CAST(b.ROLLNO AS VARCHAR))) = '' THEN 1
      ELSE 0
    END AS Missing_Rollno,

    CASE
      WHEN CAST(b.SMSNO AS VARCHAR) = CAST(b.ROLLNO AS VARCHAR) THEN 1
      ELSE 0
    END AS Same_SMSNO_Rollno

  FROM Base AS b
  LEFT JOIN vw_Duplicate_SMSNO AS d
    ON b.SCHOOL = d.SCHOOL
   AND b.CLASS = d.CLASS
   AND b.YEAR = d.YEAR
   AND b.SMSNO = d.SMSNO
),

FinalAgg AS (
  SELECT
    SCHOOL,
    CLASS,
    YEAR,
    SUM(CASE WHEN SECTION IS NULL OR SECTION = '' THEN 1 ELSE 0 END) AS Section_Missing_Count,
    SUM(CASE WHEN CATEGROY IS NULL OR CATEGROY = '' THEN 1 ELSE 0 END) AS Categroy_Missing_Count,
    SUM(CASE WHEN FATHER IS NULL OR FATHER = '' THEN 1 ELSE 0 END) AS Father_Missing_Count,
    SUM(CASE WHEN CATEGROY NOT IN ('B','DS','S') THEN 1 ELSE 0 END) AS Invalid_Categroy_Count,
    SUM(CASE WHEN [GROUP] NOT IN ('SCIENCE','PRE-MEDICAL','PRE-ENGINEERING','GENERAL SCIENCE') THEN 1 ELSE 0 END) AS Invalid_Group_Count,
    SUM(CASE WHEN SMSNO IS NULL THEN 1 ELSE 0 END) AS SMS_Missing_Count,
    SUM(IsDuplicate_SMSNO) AS Duplicate_SMSNO_Count,
    SUM(CASE WHEN cnt_rollno_school_year > 1 THEN 1 ELSE 0 END) AS Duplicate_Rollno_Count,
    SUM(CASE WHEN Incorrect_Rollno <> 0 THEN 1 ELSE 0 END) AS Incorrect_Rollno_Count,
    SUM(Missing_Rollno) AS Missing_Rollno_Count,
    SUM(Same_SMSNO_Rollno) AS Same_SMSNO_Rollno_Count
  FROM Combined
  GROUP BY
    SCHOOL,
    CLASS,
    YEAR
),

ResultMissing AS (
  SELECT
    SCHOOL,
    CLASS,
    YEAR,
    COUNT(DISTINCT ROLLNO) AS RSLT_MISSING
  FROM MissingResults
  GROUP BY
    SCHOOL,
    CLASS,
    YEAR
)

SELECT
  fa.SCHOOL,
  fa.CLASS,
  fa.YEAR,
  fa.Section_Missing_Count,
  fa.Categroy_Missing_Count,
  fa.Father_Missing_Count,
  fa.Invalid_Categroy_Count,
  fa.Invalid_Group_Count,
  fa.SMS_Missing_Count,
  ISNULL(rm.RSLT_MISSING, 0) AS RSLT_MISSING,
  fa.Duplicate_SMSNO_Count,
  fa.Duplicate_Rollno_Count,
  fa.Incorrect_Rollno_Count,
  fa.Missing_Rollno_Count,
  fa.Same_SMSNO_Rollno_Count
FROM FinalAgg AS fa
LEFT JOIN ResultMissing AS rm
  ON fa.SCHOOL = rm.SCHOOL
 AND fa.CLASS = rm.CLASS
 AND fa.YEAR = rm.YEAR;

GO

-- View: [dbo].[STUDENTS_RESULT_TOTAL] (Object ID: 1543676547)
-- Created: 2025-07-25T09:06:25.580 | Modified: 2025-07-25T09:08:06.313
CREATE VIEW [dbo].[STUDENTS_RESULT_TOTAL] AS

-- Individual subject rows
SELECT
    SR.SCHOOL,
    SR.STUDENT,
    SR.FATHER,
    SR.CLASS,
    SR.SECTION,
    SR.CATEGROY,
    SR.YEAR,
    SR.SMSNO,
    SR.ROLLNO,
    M.SUBJECT,
    M.OBTAINED,
    M.TOTAL,
    ROUND(CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0) * 100, 2) AS [%],

    CASE
        WHEN SR.CLASS IN (9,10,11,12) AND SR.YEAR IN (22,23,24)
             AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0)) * 100 > 32 THEN 'PASS'

        WHEN SR.CLASS IN (9,11) AND SR.YEAR >= 25
             AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0)) * 100 > 39 THEN 'PASS'

        -- ✅ Updated for Class 10 and 12 for Year 25
        WHEN SR.CLASS IN (10,12) AND SR.YEAR = 25
             AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0)) * 100 > 32 THEN 'PASS'

        WHEN SR.CLASS IN (6,7,8)
             AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0)) * 100 > 39 THEN 'PASS'

        ELSE 'FAIL'
    END AS STATUS,

    SR.[GROUP]

FROM STUDENTS_ROLL SR
INNER JOIN MARKS M
    ON SR.ROLLNO = M.ROLLNO AND SR.CLASS = M.CLASS AND SR.YEAR = M.YEAR

UNION ALL

-- TOTAL row per student
SELECT
    SR.SCHOOL,
    SR.STUDENT,
    SR.FATHER,
    SR.CLASS,
    SR.SECTION,
    SR.CATEGROY,
    SR.YEAR,
    SR.SMSNO,
    SR.ROLLNO,
    'TOTAL' AS SUBJECT,
    SUM(M.OBTAINED),
    SUM(M.TOTAL),
    ROUND(SUM(CAST(M.OBTAINED AS FLOAT)) / NULLIF(SUM(M.TOTAL), 0) * 100, 2),

    CASE 
        WHEN MIN(CASE 
                    WHEN SR.CLASS IN (9,10,11,12) AND SR.YEAR IN (22,23,24)
                         AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0)) * 100 > 32 THEN 1

                    WHEN SR.CLASS IN (9,11) AND SR.YEAR >= 25
                         AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0)) * 100 > 39 THEN 1

                    -- ✅ Updated for Class 10 and 12 for Year 25
                    WHEN SR.CLASS IN (10,12) AND SR.YEAR = 25
                         AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0)) * 100 > 32 THEN 1

                    WHEN SR.CLASS IN (6,7,8)
                         AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0)) * 100 > 39 THEN 1

                    ELSE 0
                END) = 1
        THEN 'PASS'
        ELSE STRING_AGG(M.SUBJECT, '-')
    END AS STATUS,

    SR.[GROUP]

FROM STUDENTS_ROLL SR
INNER JOIN MARKS M
    ON SR.ROLLNO = M.ROLLNO AND SR.CLASS = M.CLASS AND SR.YEAR = M.YEAR

GROUP BY
    SR.SCHOOL, SR.STUDENT, SR.FATHER, SR.CLASS, SR.SECTION,
    SR.CATEGROY, SR.YEAR, SR.SMSNO, SR.ROLLNO, SR.[GROUP];

GO

-- View: [dbo].[STUDENTS_RESULT_TOTAL_INTERNAL] (Object ID: 1533248517)
-- Created: 2025-11-13T19:57:43.940 | Modified: 2025-11-13T19:57:43.940
CREATE VIEW [dbo].[STUDENTS_RESULT_TOTAL_INTERNAL] AS

-- Individual subject rows
SELECT
    SR.SCHOOL,
    SR.STUDENT,
    SR.FATHER,
    SR.CLASS,
    SR.SECTION,
    SR.CATEGORY,
    SR.YEAR,
    SR.SMSNO,
    SR.ROLLNO,
    M.SUBJECT,
    CAST(M.OBTAINED AS FLOAT) AS OBTAINED,
    CAST(M.TOTAL AS FLOAT) AS TOTAL,
    ROUND(CAST(M.OBTAINED AS FLOAT) / NULLIF(CAST(M.TOTAL AS FLOAT), 0) * 100, 2) AS [%],

    CASE
        WHEN SR.CLASS IN (9,10,11,12) AND SR.YEAR IN (22,23,24)
             AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(CAST(M.TOTAL AS FLOAT), 0)) * 100 > 32 THEN 'PASS'

        WHEN SR.CLASS IN (9,11) AND SR.YEAR >= 25
             AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(CAST(M.TOTAL AS FLOAT), 0)) * 100 > 39 THEN 'PASS'

        WHEN SR.CLASS IN (10,12) AND SR.YEAR = 25
             AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(CAST(M.TOTAL AS FLOAT), 0)) * 100 > 32 THEN 'PASS'

        WHEN SR.CLASS IN (6,7,8)
             AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(CAST(M.TOTAL AS FLOAT), 0)) * 100 > 39 THEN 'PASS'

        ELSE 'FAIL'
    END AS STATUS,

    SR.[GROUP]

FROM STUDENTS_ROLL_INTERNAL_EXAM SR
INNER JOIN MARKS_INTERNAL M
    ON SR.ROLLNO = M.ROLLNO AND SR.CLASS = M.CLASS AND SR.YEAR = M.YEAR

UNION ALL

-- TOTAL row per student
SELECT
    SR.SCHOOL,
    SR.STUDENT,
    SR.FATHER,
    SR.CLASS,
    SR.SECTION,
    SR.CATEGORY,
    SR.YEAR,
    SR.SMSNO,
    SR.ROLLNO,
    'TOTAL' AS SUBJECT,
    SUM(CAST(M.OBTAINED AS FLOAT)) AS OBTAINED,
    SUM(CAST(M.TOTAL AS FLOAT)) AS TOTAL,
    ROUND(SUM(CAST(M.OBTAINED AS FLOAT)) / NULLIF(SUM(CAST(M.TOTAL AS FLOAT)), 0) * 100, 2),

    CASE 
        WHEN MIN(CASE 
                    WHEN SR.CLASS IN (9,10,11,12) AND SR.YEAR IN (22,23,24)
                         AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(CAST(M.TOTAL AS FLOAT), 0)) * 100 > 32 THEN 1

                    WHEN SR.CLASS IN (9,11) AND SR.YEAR >= 25
                         AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(CAST(M.TOTAL AS FLOAT), 0)) * 100 > 39 THEN 1

                    WHEN SR.CLASS IN (10,12) AND SR.YEAR = 25
                         AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(CAST(M.TOTAL AS FLOAT), 0)) * 100 > 32 THEN 1

                    WHEN SR.CLASS IN (6,7,8)
                         AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(CAST(M.TOTAL AS FLOAT), 0)) * 100 > 39 THEN 1

                    ELSE 0
                END) = 1
        THEN 'PASS'
        ELSE STRING_AGG(M.SUBJECT, '-')
    END AS STATUS,

    SR.[GROUP]

FROM STUDENTS_ROLL_INTERNAL_EXAM SR
INNER JOIN MARKS_INTERNAL M
    ON SR.ROLLNO = M.ROLLNO AND SR.CLASS = M.CLASS AND SR.YEAR = M.YEAR

GROUP BY
    SR.SCHOOL, SR.STUDENT, SR.FATHER, SR.CLASS, SR.SECTION,
    SR.CATEGORY, SR.YEAR, SR.SMSNO, SR.ROLLNO, SR.[GROUP];

GO

-- View: [dbo].[STUDENTS_RESULT_TOTAL_OLD] (Object ID: 443148624)
-- Created: 2025-06-17T13:15:46.460 | Modified: 2025-07-25T09:07:59.460
-- Individual subject rows
CREATE VIEW [dbo].[STUDENTS_RESULT_TOTAL_OLD] AS
SELECT
    SR.SCHOOL,
    SR.STUDENT,
    SR.FATHER,
    SR.CLASS,
    SR.SECTION,
    SR.CATEGROY,
    SR.YEAR,
    SR.SMSNO,
    SR.ROLLNO,
    M.SUBJECT,
    M.OBTAINED,
    M.TOTAL,
    ROUND(CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0) * 100, 2) AS [%],

    CASE
        WHEN SR.CLASS IN (9,10,11,12) AND SR.YEAR IN (22,23,24) AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0)) * 100 > 32 THEN 'PASS'
        WHEN SR.CLASS IN (9,11) AND SR.YEAR >= 25 AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0)) * 100 > 39 THEN 'PASS'
        WHEN SR.CLASS IN (11,12) AND SR.YEAR = 25 AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0)) * 100 > 32 THEN 'PASS'
        WHEN SR.CLASS IN (6,7,8) AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0)) * 100 > 39 THEN 'PASS'
        ELSE 'FAIL'
    END AS STATUS,

    SR.[GROUP]

FROM STUDENTS_ROLL SR
INNER JOIN MARKS M ON SR.ROLLNO = M.ROLLNO AND SR.CLASS = M.CLASS AND SR.YEAR = M.YEAR

UNION ALL

-- Total row with dynamic STATUS
SELECT
    SR.SCHOOL,
    SR.STUDENT,
    SR.FATHER,
    SR.CLASS,
    SR.SECTION,
    SR.CATEGROY,
    SR.YEAR,
    SR.SMSNO,
    SR.ROLLNO,
    'TOTAL' AS SUBJECT,
    SUM(M.OBTAINED),
    SUM(M.TOTAL),
    ROUND(SUM(CAST(M.OBTAINED AS FLOAT)) / NULLIF(SUM(M.TOTAL), 0) * 100, 2),

    CASE 
        WHEN MIN(CASE 
                    WHEN SR.CLASS IN (9,10,11,12) AND SR.YEAR IN (22,23,24) AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0)) * 100 > 32 THEN 1
                    WHEN SR.CLASS IN (9,11) AND SR.YEAR >= 25 AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0)) * 100 > 39 THEN 1
                    WHEN SR.CLASS IN (11,12) AND SR.YEAR = 25 AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0)) * 100 > 32 THEN 1
                    WHEN SR.CLASS IN (6,7,8) AND (CAST(M.OBTAINED AS FLOAT) / NULLIF(M.TOTAL, 0)) * 100 > 39 THEN 1
                    ELSE 0
                END) = 1
        THEN 'PASS'
        ELSE STRING_AGG(M.SUBJECT, '-') 
    END AS STATUS,

    SR.[GROUP]

FROM STUDENTS_ROLL SR
INNER JOIN MARKS M ON SR.ROLLNO = M.ROLLNO AND SR.CLASS = M.CLASS AND SR.YEAR = M.YEAR

GROUP BY SR.SCHOOL, SR.STUDENT, SR.FATHER, SR.CLASS, SR.SECTION, SR.CATEGROY, SR.YEAR, SR.SMSNO, SR.ROLLNO, SR.[GROUP];

GO

-- View: [dbo].[STUDENT_TEACHER_EXAM_MARKS_VIEW] (Object ID: 1945773989)
-- Created: 2025-12-05T10:35:25.480 | Modified: 2026-01-29T23:46:31.047
CREATE VIEW [dbo].[STUDENT_TEACHER_EXAM_MARKS_VIEW] AS
SELECT 
    T3.SUBJECT, 
    T3."TOTAL MARKS" AS "TOTAL",
    CAST(NULL AS DECIMAL) AS OBTAINED, 
    CAST(NULL AS DECIMAL) AS "PERCENTAGE", 
    CAST(NULL AS VARCHAR(10)) AS GRADE, 
    CAST(NULL AS VARCHAR(10)) AS STATUS,
    T2.ROLLNO, 
    T2.STUDENT AS "STUDENT NAME", 
    T2.FATHER AS "FATHER NAME",
    T2.CLASS, 
    T2.SECTION, 
    T2.SCHOOL, 
    T2."GROUP", 
    T2.YEAR,
    T1.EXAM AS "EXAMTYPE"
FROM STUDENTS_ROLL_INTERNAL_EXAM T2
INNER JOIN SUBJECT_GORUP_YEAR_MARKS_26 T3 
    ON T2.CLASS = T3.CLASS 
    AND T2."GROUP" = T3."GROUP" 
    AND T2.YEAR = T3.YEAR
    -- ADDED: Join on EXAM to pull the correct Total Marks for MOCK1, MOCK2, etc.
    AND T2.EXAM = T3.EXAM 
INNER JOIN (
    SELECT CLASS, SECTION, SUBJECT, YEAR, EXAM,
    ROW_NUMBER() OVER (PARTITION BY CLASS, SECTION, SUBJECT, YEAR, EXAM ORDER BY EID) as rn
    FROM TEACHERS_INTERNAL_EXAM
) AS T1 
    ON T2.CLASS = T1.CLASS 
    AND T3.SUBJECT = T1.SUBJECT 
    AND T2.YEAR = T1.YEAR 
    AND T2.SECTION = T1.SECTION 
    AND T2.EXAM = T1.EXAM 
    AND T1.rn = 1;

GO

-- View: [dbo].[School_Ind_Pos] (Object ID: 1211151360)
-- Created: 2025-06-29T19:10:55.550 | Modified: 2025-06-29T19:10:55.550
CREATE VIEW [dbo].[School_Ind_Pos] AS
WITH TotalRows AS (
    SELECT
        SCHOOL,
        YEAR,
        CLASS,
        ROLLNO,
        OBTAINED,
        TOTAL,
        [%]
    FROM students_result_total
    WHERE SUBJECT = 'TOTAL'
),

SchoolClassStats AS (
    SELECT
        SCHOOL,
        YEAR,
        CLASS,
        COUNT(DISTINCT ROLLNO) AS Strength,
        SUM(OBTAINED) AS SumObtained,
        SUM(TOTAL) AS SumTotal,
        CAST(SUM(OBTAINED) * 100.0 / NULLIF(SUM(TOTAL), 0) AS DECIMAL(6,2)) AS AggregatePercentage,
        SUM(CASE WHEN [%] >= 90 AND [%] <= 100 THEN 1 ELSE 0 END) AS [>90],
        SUM(CASE WHEN [%] >= 80 AND [%] < 90 THEN 1 ELSE 0 END) AS [>80],
        SUM(CASE WHEN [%] >= 70 AND [%] < 80 THEN 1 ELSE 0 END) AS [>70],
        SUM(CASE WHEN [%] >= 60 AND [%] < 70 THEN 1 ELSE 0 END) AS [>60],
        SUM(CASE WHEN [%] >= 50 AND [%] < 60 THEN 1 ELSE 0 END) AS [>50],
        SUM(CASE WHEN [%] >= 40 AND [%] < 50 THEN 1 ELSE 0 END) AS [>40],
        SUM(CASE WHEN [%] < 40 THEN 1 ELSE 0 END) AS [<40]
    FROM TotalRows
    GROUP BY
        SCHOOL, YEAR, CLASS
),

RankedSchools AS (
    SELECT
        SCHOOL,
        YEAR,
        CLASS,
        Strength,
        SumObtained,
        SumTotal,
        AggregatePercentage,
        [>90],
        [>80],
        [>70],
        [>60],
        [>50],
        [>40],
        [<40],
        RANK() OVER (
            PARTITION BY YEAR, CLASS
            ORDER BY AggregatePercentage DESC
        ) AS Position
    FROM SchoolClassStats
)

SELECT
    SCHOOL,
    YEAR,
    CLASS,
    Strength,
    SumObtained,
    SumTotal,
    AggregatePercentage,
    [>90],
    [>80],
    [>70],
    [>60],
    [>50],
    [>40],
    [<40],
    Position
FROM RankedSchools;

GO

-- View: [dbo].[School_Ind_Pos_SUB] (Object ID: 816721962)
-- Created: 2025-10-07T09:15:46.213 | Modified: 2025-10-07T09:15:46.213
CREATE VIEW [dbo].[School_Ind_Pos_SUB] AS
WITH TotalRows AS (
    SELECT
        SCHOOL,
        YEAR,
        CLASS,
        ROLLNO,
        OBTAINED,
        TOTAL,
        [%]
    FROM students_result_total
    WHERE SUBJECT = 'TOTAL'
),

Below33Stats AS (
    SELECT
        SCHOOL,
        YEAR,
        CLASS,
        COUNT(*) AS Below33Count
    FROM students_result_total
    WHERE [%] < 33
    GROUP BY SCHOOL, YEAR, CLASS
),

SchoolClassStats AS (
    SELECT
        SCHOOL,
        YEAR,
        CLASS,
        COUNT(DISTINCT ROLLNO) AS Strength,
        SUM(OBTAINED) AS SumObtained,
        SUM(TOTAL) AS SumTotal,
        CAST(SUM(OBTAINED) * 100.0 / NULLIF(SUM(TOTAL), 0) AS DECIMAL(6,2)) AS AggregatePercentage,
        SUM(CASE WHEN [%] >= 90 AND [%] <= 100 THEN 1 ELSE 0 END) AS [>90],
        SUM(CASE WHEN [%] >= 80 AND [%] < 90 THEN 1 ELSE 0 END) AS [>80],
        SUM(CASE WHEN [%] >= 70 AND [%] < 80 THEN 1 ELSE 0 END) AS [>70],
        SUM(CASE WHEN [%] >= 60 AND [%] < 70 THEN 1 ELSE 0 END) AS [>60],
        SUM(CASE WHEN [%] >= 50 AND [%] < 60 THEN 1 ELSE 0 END) AS [>50],
        SUM(CASE WHEN [%] >= 40 AND [%] < 50 THEN 1 ELSE 0 END) AS [>40],
        SUM(CASE WHEN [%] < 40 THEN 1 ELSE 0 END) AS [<40]
    FROM TotalRows
    GROUP BY SCHOOL, YEAR, CLASS
),

RankedSchools AS (
    SELECT
        S.SCHOOL,
        S.YEAR,
        S.CLASS,
        S.Strength,
        S.SumObtained,
        S.SumTotal,
        S.AggregatePercentage,
        S.[>90],
        S.[>80],
        S.[>70],
        S.[>60],
        S.[>50],
        S.[>40],
        S.[<40],
        ISNULL(B.Below33Count, 0) AS Below33Count,
        RANK() OVER (
            PARTITION BY S.YEAR, S.CLASS
            ORDER BY S.AggregatePercentage DESC
        ) AS Position
    FROM SchoolClassStats AS S
    LEFT JOIN Below33Stats AS B
        ON S.SCHOOL = B.SCHOOL
        AND S.YEAR = B.YEAR
        AND S.CLASS = B.CLASS
)

SELECT
    SCHOOL,
    YEAR,
    CLASS,
    Strength,
    SumObtained,
    SumTotal,
    AggregatePercentage,
    [>90],
    [>80],
    [>70],
    [>60],
    [>50],
    [>40],
    [<40],
    Below33Count AS [Subjects <33%],
    Position
FROM RankedSchools;

GO

-- View: [dbo].[School_avg_pos] (Object ID: 1227151417)
-- Created: 2025-06-29T19:23:24.523 | Modified: 2025-06-29T19:23:24.523
CREATE VIEW [dbo].[School_avg_pos] AS
SELECT
    SCHOOL,
    CLASS,
    SUM(SumObtained) AS OBTAINED,
    SUM(SumTotal) AS TOTAL,
    CAST(SUM(SumObtained) * 100.0 / NULLIF(SUM(SumTotal), 0) AS DECIMAL(6,2)) AS [%],
    CAST(AVG(CAST(Position AS FLOAT)) AS DECIMAL(6,2)) AS [AVG-POS]
FROM School_Ind_Pos
GROUP BY
    SCHOOL,
    CLASS;

GO

-- View: [dbo].[TEACHER_MARK_ENTRY_VIEW] (Object ID: 438292621)
-- Created: 2025-12-15T03:13:49.100 | Modified: 2025-12-15T03:29:04.083
-- Use ALTER VIEW to modify the existing view definition
CREATE VIEW [dbo].[TEACHER_MARK_ENTRY_VIEW]
AS
SELECT
    -- ---------------------------------------
    -- 1. IDENTIFYING/FILTERING COLUMNS (from View B)
    -- ---------------------------------------
    B.ROLLNO,
    B.[STUDENT NAME],
    B.[FATHER NAME],
    B.CLASS,
    B.SECTION,
    B.SCHOOL,
    B.[GROUP],
    B.YEAR,
    B.EXAMTYPE,
    
    -- ---------------------------------------
    -- 2. ROSTER/SUBJECT DATA (from View B)
    -- ---------------------------------------
    B.SUBJECT,
    B.TOTAL,
    
    -- ---------------------------------------
    -- 3. SAVED MARKS DATA (All columns from Table C, marks_internal)
    -- ---------------------------------------
    C.ID AS Marks_ID,
    ISNULL(C.OBTAINED, 0.00) AS Entered_OBTAINED,
    C.OBTAINED AS Actual_Saved_Obtained,
    C.[%] AS Marks_Percentage,
    C.GRADE AS Marks_Grade,
    C.STATUS AS Marks_Status,
    C.Remarks,
    
    CASE WHEN C.ID IS NOT NULL THEN 'Y' ELSE 'N' END AS Marks_Entered_Flag

FROM
    STUDENT_TEACHER_EXAM_MARKS_VIEW AS B
LEFT JOIN
    marks_internal AS C
ON
    B.ROLLNO = C.ROLLNO AND
    B.CLASS = C.CLASS AND
    B.YEAR = C.YEAR AND
    B.SUBJECT = C.SUBJECT AND
    B.EXAMTYPE = C.EXAMTYPE
-- The ORDER BY clause is typically NOT included directly in a view definition 
-- in SQL Server (and most other databases).

-- A view only defines the structure and the rows retrieved.
-- Sorting is applied when you SELECT * FROM the view.

-- I will include a note here for clarity, but you should apply the ORDER BY 
-- in your ASP.NET application's query for best performance.
/*
--- IMPORTANT NOTE ON ORDER BY ---
In SQL Server, you generally cannot use ORDER BY in a view unless the 
TOP clause is also present. For best practice, you should apply the 
ORDER BY clause when your application queries the view:
SELECT * FROM TEACHER_MARK_ENTRY_VIEW ORDER BY ROLLNO, SUBJECT;
*/

GO

-- View: [dbo].[TEACHER_SUBJECT_INCORRECT] (Object ID: 187147712)
-- Created: 2025-06-15T11:44:53.300 | Modified: 2025-06-15T11:44:53.300
CREATE VIEW [dbo].[TEACHER_SUBJECT_INCORRECT] AS
SELECT 
    T.SCHOOL, 
    T.YEAR, 
    T.CLASS, 
    T.SECTION, 
    T.SUBJECT AS Incorrect_Subject
FROM 
    TEAHCERS AS T
LEFT JOIN 
    CorrectSubjects AS CS 
    ON T.CLASS = CS.CLASS 
    AND LTRIM(RTRIM(T.SUBJECT)) = CS.SUBJECT
WHERE 
    CS.SUBJECT IS NULL
GROUP BY 
    T.SCHOOL, 
    T.YEAR, 
    T.CLASS, 
    T.SECTION, 
    T.SUBJECT;

GO

-- View: [dbo].[TOP3_ALL_SCHOOL] (Object ID: 1255675521)
-- Created: 2025-07-23T22:59:55.383 | Modified: 2025-07-23T22:59:55.383
CREATE VIEW [dbo].[TOP3_ALL_SCHOOL] AS
SELECT 
  STUDENT,
  FATHER,
  CLASS,
  YEAR,
  SCHOOL,
  OBTAINED,
  [%],
  RANK() OVER (
    PARTITION BY SCHOOL, CLASS, YEAR 
    ORDER BY [%] DESC
  ) AS RankInSchool
FROM STUDENTS_RESULT_TOTAL
WHERE SUBJECT = 'TOTAL';

GO

-- View: [dbo].[TR2] (Object ID: 1015674666)
-- Created: 2025-07-22T11:37:15.197 | Modified: 2025-07-22T11:42:49.197
CREATE   VIEW [dbo].[TR2] AS

-- 1️⃣ Regular categories: B, DS, S
SELECT 
    T.EID,
    T.NAME,
    Q.SCHOOL,
    Q.EXAMTYPE,
    Q.SUBJECT,
    Q.CLASS,
    Q.SECTION,
    Q.Year,
    Q.CATEGROY,
    Q.STRENGTH,
    Q.Count_90_100,
    Q.Count_80_90,
    Q.Count_70_80,
    Q.Count_60_70,
    Q.Count_50_60,
    Q.Count_40_50,
    Q.Count_0_39,
    Q.APPEARED,
    Q.PASSED,
    Q.[PASS%],
    Q.[CLASS AVG]
FROM Query1 Q
JOIN TEAHCERS T
    ON Q.YEAR = T.YEAR
   AND Q.CLASS = T.CLASS
   AND Q.SECTION = T.SECTION
   AND Q.SUBJECT = T.SUBJECT
   AND Q.SCHOOL = T.SCHOOL
WHERE Q.CATEGROY IN ('B', 'DS', 'S')

UNION ALL

-- 2️⃣ Aggregated category: ALL
SELECT 
    T.EID,
    T.NAME,
    Agg.SCHOOL,
    MAX(Q.EXAMTYPE),
    Agg.SUBJECT,
    Agg.CLASS,
    Agg.SECTION,
    Agg.Year,
    'ALL' AS CATEGROY,
    SUM(Q.STRENGTH),
    SUM(Q.Count_90_100),
    SUM(Q.Count_80_90),
    SUM(Q.Count_70_80),
    SUM(Q.Count_60_70),
    SUM(Q.Count_50_60),
    SUM(Q.Count_40_50),
    SUM(Q.Count_0_39),
    SUM(Q.APPEARED),
    SUM(Q.PASSED),
    CAST(
        CASE WHEN SUM(Q.APPEARED) > 0 
             THEN ROUND((SUM(Q.PASSED) * 100.0) / SUM(Q.APPEARED), 2)
             ELSE 0
        END AS DECIMAL(5,2)
    ) AS [PASS%],
    CAST(
        CASE WHEN SUM(Q.APPEARED) > 0
             THEN ROUND(SUM(Q.[CLASS AVG] * Q.APPEARED) / SUM(Q.APPEARED), 2)
             ELSE 0
        END AS DECIMAL(5,2)
    ) AS [CLASS AVG]
FROM Query1 Q
JOIN (
    SELECT DISTINCT CLASS, SECTION, SUBJECT, YEAR, SCHOOL
    FROM Query1
    WHERE CATEGROY IN ('B', 'DS', 'S')
) Agg
    ON Q.CLASS = Agg.CLASS
   AND Q.SECTION = Agg.SECTION
   AND Q.SUBJECT = Agg.SUBJECT
   AND Q.YEAR = Agg.YEAR
   AND Q.SCHOOL = Agg.SCHOOL
JOIN TEAHCERS T
    ON T.CLASS = Agg.CLASS
   AND T.SECTION = Agg.SECTION
   AND T.SUBJECT = Agg.SUBJECT
   AND T.YEAR = Agg.YEAR
   AND T.SCHOOL = Agg.SCHOOL
WHERE Q.CATEGROY IN ('B', 'DS', 'S')
GROUP BY 
    T.EID, T.NAME,
    Agg.CLASS, Agg.SECTION, Agg.SUBJECT, Agg.YEAR, Agg.SCHOOL;

GO

-- View: [dbo].[TR2_Prac] (Object ID: 1783677402)
-- Created: 2025-07-26T10:36:50.517 | Modified: 2025-07-26T10:36:50.517
CREATE VIEW [dbo].[TR2_Prac] AS

-- 1️⃣ Regular categories: B, DS, S
SELECT 
    T.EID,
    T.NAME,
    Q.SCHOOL,
    Q.EXAMTYPE,
    Q.SUBJECT,
    Q.CLASS,
    Q.SECTION,
    Q.Year,
    Q.CATEGROY,
    Q.STRENGTH,
    Q.Count_90_100,
    Q.Count_80_90,
    Q.Count_70_80,
    Q.Count_60_70,
    Q.Count_50_60,
    Q.Count_40_50,
    Q.Count_0_39,
    Q.APPEARED,
    Q.PASSED,
    Q.[PASS%],
    Q.[CLASS AVG]
FROM Query1_Prac Q
JOIN TEAHCERS T
    ON Q.YEAR = T.YEAR
   AND Q.CLASS = T.CLASS
   AND Q.SECTION = T.SECTION
   AND Q.SUBJECT = T.SUBJECT
   AND Q.SCHOOL = T.SCHOOL
WHERE Q.CATEGROY IN ('B', 'DS', 'S')

UNION ALL

-- 2️⃣ Aggregated category: ALL
SELECT 
    T.EID,
    T.NAME,
    Agg.SCHOOL,
    MAX(Q.EXAMTYPE),
    Agg.SUBJECT,
    Agg.CLASS,
    Agg.SECTION,
    Agg.Year,
    'ALL' AS CATEGROY,
    SUM(Q.STRENGTH),
    SUM(Q.Count_90_100),
    SUM(Q.Count_80_90),
    SUM(Q.Count_70_80),
    SUM(Q.Count_60_70),
    SUM(Q.Count_50_60),
    SUM(Q.Count_40_50),
    SUM(Q.Count_0_39),
    SUM(Q.APPEARED),
    SUM(Q.PASSED),
    CAST(
        CASE WHEN SUM(Q.APPEARED) > 0 
             THEN ROUND((SUM(Q.PASSED) * 100.0) / SUM(Q.APPEARED), 2)
             ELSE 0
        END AS DECIMAL(5,2)
    ) AS [PASS%],
    CAST(
        CASE WHEN SUM(Q.APPEARED) > 0
             THEN ROUND(SUM(Q.[CLASS AVG] * Q.APPEARED) / SUM(Q.APPEARED), 2)
             ELSE 0
        END AS DECIMAL(5,2)
    ) AS [CLASS AVG]
FROM Query1_Prac Q
JOIN (
    SELECT DISTINCT CLASS, SECTION, SUBJECT, YEAR, SCHOOL
    FROM Query1_Prac
    WHERE CATEGROY IN ('B', 'DS', 'S')
) Agg
    ON Q.CLASS = Agg.CLASS
   AND Q.SECTION = Agg.SECTION
   AND Q.SUBJECT = Agg.SUBJECT
   AND Q.YEAR = Agg.YEAR
   AND Q.SCHOOL = Agg.SCHOOL
JOIN TEAHCERS T
    ON T.CLASS = Agg.CLASS
   AND T.SECTION = Agg.SECTION
   AND T.SUBJECT = Agg.SUBJECT
   AND T.YEAR = Agg.YEAR
   AND T.SCHOOL = Agg.SCHOOL
WHERE Q.CATEGROY IN ('B', 'DS', 'S')
GROUP BY 
    T.EID, T.NAME,
    Agg.CLASS, Agg.SECTION, Agg.SUBJECT, Agg.YEAR, Agg.SCHOOL;

GO

-- View: [dbo].[TR2_Theory] (Object ID: 1767677345)
-- Created: 2025-07-26T10:35:46.727 | Modified: 2025-07-26T10:35:46.727
CREATE VIEW [dbo].[TR2_Theory] AS

-- 1️⃣ Regular categories: B, DS, S
SELECT 
    T.EID,
    T.NAME,
    Q.SCHOOL,
    Q.EXAMTYPE,
    Q.SUBJECT,
    Q.CLASS,
    Q.SECTION,
    Q.Year,
    Q.CATEGROY,
    Q.STRENGTH,
    Q.Count_90_100,
    Q.Count_80_90,
    Q.Count_70_80,
    Q.Count_60_70,
    Q.Count_50_60,
    Q.Count_40_50,
    Q.Count_0_39,
    Q.APPEARED,
    Q.PASSED,
    Q.[PASS%],
    Q.[CLASS AVG]
FROM Query1_theory Q
JOIN TEAHCERS T
    ON Q.YEAR = T.YEAR
   AND Q.CLASS = T.CLASS
   AND Q.SECTION = T.SECTION
   AND Q.SUBJECT = T.SUBJECT
   AND Q.SCHOOL = T.SCHOOL
WHERE Q.CATEGROY IN ('B', 'DS', 'S')

UNION ALL

-- 2️⃣ Aggregated category: ALL
SELECT 
    T.EID,
    T.NAME,
    Agg.SCHOOL,
    MAX(Q.EXAMTYPE),
    Agg.SUBJECT,
    Agg.CLASS,
    Agg.SECTION,
    Agg.Year,
    'ALL' AS CATEGROY,
    SUM(Q.STRENGTH),
    SUM(Q.Count_90_100),
    SUM(Q.Count_80_90),
    SUM(Q.Count_70_80),
    SUM(Q.Count_60_70),
    SUM(Q.Count_50_60),
    SUM(Q.Count_40_50),
    SUM(Q.Count_0_39),
    SUM(Q.APPEARED),
    SUM(Q.PASSED),
    CAST(
        CASE WHEN SUM(Q.APPEARED) > 0 
             THEN ROUND((SUM(Q.PASSED) * 100.0) / SUM(Q.APPEARED), 2)
             ELSE 0
        END AS DECIMAL(5,2)
    ) AS [PASS%],
    CAST(
        CASE WHEN SUM(Q.APPEARED) > 0
             THEN ROUND(SUM(Q.[CLASS AVG] * Q.APPEARED) / SUM(Q.APPEARED), 2)
             ELSE 0
        END AS DECIMAL(5,2)
    ) AS [CLASS AVG]
FROM Query1_theory Q
JOIN (
    SELECT DISTINCT CLASS, SECTION, SUBJECT, YEAR, SCHOOL
    FROM Query1_theory
    WHERE CATEGROY IN ('B', 'DS', 'S')
) Agg
    ON Q.CLASS = Agg.CLASS
   AND Q.SECTION = Agg.SECTION
   AND Q.SUBJECT = Agg.SUBJECT
   AND Q.YEAR = Agg.YEAR
   AND Q.SCHOOL = Agg.SCHOOL
JOIN TEAHCERS T
    ON T.CLASS = Agg.CLASS
   AND T.SECTION = Agg.SECTION
   AND T.SUBJECT = Agg.SUBJECT
   AND T.YEAR = Agg.YEAR
   AND T.SCHOOL = Agg.SCHOOL
WHERE Q.CATEGROY IN ('B', 'DS', 'S')
GROUP BY 
    T.EID, T.NAME,
    Agg.CLASS, Agg.SECTION, Agg.SUBJECT, Agg.YEAR, Agg.SCHOOL;

GO

-- View: [dbo].[TR_ALL_DEDUCTED] (Object ID: 1726629194)
-- Created: 2025-06-10T19:53:31.403 | Modified: 2025-06-10T19:53:31.403
CREATE VIEW [dbo].[TR_ALL_DEDUCTED] AS
SELECT
    *,
    (APPEARED - PASSED) AS FAIL,
    (APPEARED - PASSED) * 0.50 AS DEDUCTION
FROM TR_ALL;

GO

-- View: [dbo].[TR_ALL_IND_POS] (Object ID: 254623950)
-- Created: 2025-05-22T20:26:54.673 | Modified: 2025-05-24T09:50:41.010
CREATE VIEW [dbo].[TR_ALL_IND_POS] AS
WITH RankedData AS (
    SELECT
        EID,
        NAME,
        SCHOOL,
        EXAMTYPE,
        SUBJECT,
        CLASS,
        SECTION,
        Year,
        CATEGROY,
        STRENGTH,
        Count_90_100,
        Count_80_90,
        Count_70_80,
        Count_60_70,
        Count_50_60,
        Count_40_50,
        Count_0_39,
        APPEARED,
        PASSED,
        [PASS%] AS PASS_PERCENT,
        [CLASS AVG] AS CLASS_AVG,
        (ISNULL(Count_90_100, 0) + ISNULL(Count_80_90, 0) + ISNULL(Count_70_80, 0)) AS Above_70,
        (ISNULL(Count_60_70, 0) + ISNULL(Count_50_60, 0) + ISNULL(Count_40_50, 0) + ISNULL(Count_0_39, 0)) AS Below_70,
        COUNT(*) OVER (PARTITION BY EID, Year) AS WL,
        COUNT(*) OVER (
            PARTITION BY CLASS, Year, UPPER(LTRIM(RTRIM(SUBJECT)))
        ) AS TOTAL_POSITIONS,
        CAST(RANK() OVER (
            PARTITION BY CLASS, Year, UPPER(LTRIM(RTRIM(SUBJECT)))
            ORDER BY [CLASS AVG] DESC
        ) AS INT) AS Position
    FROM TR_ALL
    WHERE CATEGROY = 'ALL'
)

SELECT
    RD.EID,
    RD.NAME,
    RD.SCHOOL,
    RD.EXAMTYPE,
    RD.SUBJECT,
    RD.CLASS,
    RD.SECTION,
    RD.Year,
    RD.CATEGROY,
    RD.STRENGTH,
    RD.Count_90_100,
    RD.Count_80_90,
    RD.Count_70_80,
    RD.Count_60_70,
    RD.Count_50_60,
    RD.Count_40_50,
    RD.Count_0_39,
    RD.Above_70,
    RD.Below_70,
    RD.APPEARED,
    RD.PASSED,
    RD.PASS_PERCENT AS [PASS%],
    RD.CLASS_AVG AS [CLASS AVG],
    RD.Position,
    RD.TOTAL_POSITIONS,
    RD.WL,

    -- SCHOOL-MERGE
    (
        SELECT STRING_AGG(SCHOOL, '-') 
        FROM (
            SELECT DISTINCT SCHOOL 
            FROM TR_ALL 
            WHERE EID = RD.EID AND Year = RD.Year
        ) AS SchoolList
    ) AS [SCHOOL-MERGE],

    -- SUBJECT_MERGE
    (
        SELECT STRING_AGG(abbreviation, '-') 
        FROM (
            SELECT DISTINCT CS.abbreviation
            FROM TR_ALL T
            INNER JOIN CorrectSubjects CS 
                ON UPPER(LTRIM(RTRIM(T.SUBJECT))) = UPPER(LTRIM(RTRIM(CS.subject)))
            WHERE T.EID = RD.EID AND T.Year = RD.Year
        ) AS SubjectList
    ) AS SUBJECT_MERGE

FROM RankedData RD;

GO

-- View: [dbo].[TR_ALL_IND_POS_16] (Object ID: 94623380)
-- Created: 2025-05-20T09:11:55.563 | Modified: 2025-05-24T09:50:29.270
CREATE VIEW [dbo].[TR_ALL_IND_POS_16] AS
WITH RankedData AS (
    SELECT
        EID,
        NAME,
        SCHOOL,
        EXAMTYPE,
        SUBJECT,
        CLASS,
        SECTION,
        Year,
        CATEGROY,
        STRENGTH,
        Count_90_100,
        Count_80_90,
        Count_70_80,
        Count_60_70,
        Count_50_60,
        Count_40_50,
        Count_0_39,
        APPEARED,
        PASSED,
        [PASS%] AS PASS_PERCENT,
        [CLASS AVG] AS CLASS_AVG,
        (ISNULL(Count_90_100, 0) + ISNULL(Count_80_90, 0) + ISNULL(Count_70_80, 0)) AS Above_70,
        (ISNULL(Count_60_70, 0) + ISNULL(Count_50_60, 0) + ISNULL(Count_40_50, 0) + ISNULL(Count_0_39, 0)) AS Below_70,
        COUNT(*) OVER (PARTITION BY EID, Year) AS WL,
        COUNT(*) OVER (
            PARTITION BY 
                CASE 
                    WHEN CLASS IN (6,7,8) THEN CONCAT(CLASS, '_', Year, '_', UPPER(LTRIM(RTRIM(SUBJECT))), '_', 
                        CASE WHEN UPPER(LTRIM(RTRIM(SECTION))) IN ('C','D') THEN 'C_D' 
                             ELSE UPPER(LTRIM(RTRIM(SECTION))) END)
                    WHEN CLASS IN (9,10) AND UPPER(LTRIM(RTRIM(SUBJECT))) NOT IN ('COMPUTER SCIENCE','BIOLOGY') THEN 
                        CONCAT(CLASS, '_', Year, '_', UPPER(LTRIM(RTRIM(SUBJECT))), '_', 
                        CASE WHEN UPPER(LTRIM(RTRIM(SECTION))) IN ('C','D') THEN 'C_D' 
                             ELSE UPPER(LTRIM(RTRIM(SECTION))) END)
                    WHEN CLASS IN (9,10) THEN CONCAT(CLASS, '_', Year, '_', UPPER(LTRIM(RTRIM(SUBJECT))))
                    WHEN CLASS IN (11,12) AND UPPER(LTRIM(RTRIM(SUBJECT))) IN 
                        ('BIOLOGY','COMPUTER SCIENCE','MATHEMATICS','CHEMISTRY') THEN 
                        CONCAT(CLASS, '_', Year, '_', UPPER(LTRIM(RTRIM(SUBJECT))))
                    WHEN CLASS IN (11,12) THEN CONCAT(CLASS, '_', Year, '_', UPPER(LTRIM(RTRIM(SUBJECT))), '_', 
                        CASE WHEN UPPER(LTRIM(RTRIM(SECTION))) IN ('C','D') THEN 'C_D' 
                             ELSE UPPER(LTRIM(RTRIM(SECTION))) END)
                    ELSE 'OTHER'
                END
        ) AS TOTAL_POSITIONS,
        CAST(RANK() OVER (
            PARTITION BY 
                CASE 
                    WHEN CLASS IN (6,7,8) THEN CONCAT(CLASS, '_', Year, '_', UPPER(LTRIM(RTRIM(SUBJECT))), '_', 
                        CASE WHEN UPPER(LTRIM(RTRIM(SECTION))) IN ('C','D') THEN 'C_D' 
                             ELSE UPPER(LTRIM(RTRIM(SECTION))) END)
                    WHEN CLASS IN (9,10) AND UPPER(LTRIM(RTRIM(SUBJECT))) NOT IN ('COMPUTER SCIENCE','BIOLOGY') THEN 
                        CONCAT(CLASS, '_', Year, '_', UPPER(LTRIM(RTRIM(SUBJECT))), '_', 
                        CASE WHEN UPPER(LTRIM(RTRIM(SECTION))) IN ('C','D') THEN 'C_D' 
                             ELSE UPPER(LTRIM(RTRIM(SECTION))) END)
                    WHEN CLASS IN (9,10) THEN CONCAT(CLASS, '_', Year, '_', UPPER(LTRIM(RTRIM(SUBJECT))))
                    WHEN CLASS IN (11,12) AND UPPER(LTRIM(RTRIM(SUBJECT))) IN 
                        ('BIOLOGY','COMPUTER SCIENCE','MATHEMATICS','CHEMISTRY') THEN 
                        CONCAT(CLASS, '_', Year, '_', UPPER(LTRIM(RTRIM(SUBJECT))))
                    WHEN CLASS IN (11,12) THEN CONCAT(CLASS, '_', Year, '_', UPPER(LTRIM(RTRIM(SUBJECT))), '_', 
                        CASE WHEN UPPER(LTRIM(RTRIM(SECTION))) IN ('C','D') THEN 'C_D' 
                             ELSE UPPER(LTRIM(RTRIM(SECTION))) END)
                    ELSE 'OTHER'
                END
            ORDER BY [CLASS AVG] DESC
        ) AS INT) AS Position
    FROM TR_ALL
    WHERE CATEGROY = 'ALL'
)
SELECT
    RD.EID,
    RD.NAME,
    RD.SCHOOL,
    RD.EXAMTYPE,
    RD.SUBJECT,
    RD.CLASS,
    RD.SECTION,
    RD.Year,
    RD.CATEGROY,
    RD.STRENGTH,
    RD.Count_90_100,
    RD.Count_80_90,
    RD.Count_70_80,
    RD.Count_60_70,
    RD.Count_50_60,
    RD.Count_40_50,
    RD.Count_0_39,
    RD.Above_70,
    RD.Below_70,
    RD.APPEARED,
    RD.PASSED,
    RD.PASS_PERCENT AS [PASS%],
    RD.CLASS_AVG AS [CLASS AVG],
    RD.Position,
    RD.TOTAL_POSITIONS,
    RD.WL,
   -- SCHOOL-MERGE
(
    SELECT STRING_AGG(SCHOOL, '-') 
    FROM (
        SELECT DISTINCT SCHOOL 
        FROM TR_ALL 
        WHERE EID = RD.EID AND Year = RD.Year
    ) AS SchoolList
) AS [SCHOOL-MERGE],

-- SUBJECT_MERGE
(
    SELECT STRING_AGG(abbreviation, '-') 
    FROM (
        SELECT DISTINCT CS.abbreviation
        FROM TR_ALL T
        INNER JOIN CorrectSubjects CS 
            ON UPPER(LTRIM(RTRIM(T.SUBJECT))) = UPPER(LTRIM(RTRIM(CS.subject)))
        WHERE T.EID = RD.EID AND T.Year = RD.Year
    ) AS SubjectList
) AS SUBJECT_MERGE

FROM RankedData RD;

GO

-- View: [dbo].[TR_ALL_SECTIONS_POS] (Object ID: 285244071)
-- Created: 2025-10-21T11:23:59.597 | Modified: 2025-10-21T11:25:13.963
CREATE VIEW [dbo].[TR_ALL_SECTIONS_POS] AS
WITH RankedData AS (
    SELECT
        T.EID,
        T.NAME,
        T.SCHOOL,
        T.EXAMTYPE,
        T.SUBJECT,
        T.CLASS,
        T.SECTION,
        T.Year,
        T.CATEGROY,
        T.STRENGTH,
        T.Count_90_100,
        T.Count_80_90,
        T.Count_70_80,
        T.Count_60_70,
        T.Count_50_60,
        T.Count_40_50,
        T.Count_0_39,
        T.APPEARED,
        T.PASSED,
        T.[PASS%] AS PASS_PERCENT,

        -- 🔹 Pick CLASS AVG from vTeacher_all_sec_per
        V.[%] AS CLASS_AVG,

        (ISNULL(T.Count_90_100, 0) + ISNULL(T.Count_80_90, 0) + ISNULL(T.Count_70_80, 0)) AS Above_70,
        (ISNULL(T.Count_60_70, 0) + ISNULL(T.Count_50_60, 0) + ISNULL(T.Count_40_50, 0) + ISNULL(T.Count_0_39, 0)) AS Below_70,

        COUNT(*) OVER (PARTITION BY T.EID, T.Year) AS WL,
        COUNT(*) OVER (PARTITION BY T.CLASS, T.Year, UPPER(LTRIM(RTRIM(T.SUBJECT)))) AS TOTAL_POSITIONS,

        CAST(RANK() OVER (
            PARTITION BY T.CLASS, T.Year, UPPER(LTRIM(RTRIM(T.SUBJECT)))
            ORDER BY V.[%] DESC
        ) AS INT) AS Position

    FROM TR_ALL AS T
    LEFT JOIN vTeacher_all_sec_per AS V
        ON T.EID = V.EID
        AND T.CLASS = V.CLASS
        AND T.YEAR = V.YEAR
        AND UPPER(LTRIM(RTRIM(T.SUBJECT))) = UPPER(LTRIM(RTRIM(V.SUBJECT)))
    WHERE T.CATEGROY = 'ALL'
)

SELECT
    RD.EID,
    RD.NAME,
    RD.SCHOOL,
    RD.EXAMTYPE,
    RD.SUBJECT,
    RD.CLASS,
    'ALL' AS SECTION,
    RD.Year,
    'ALL SEC CAT' AS CATEGROY,

    SUM(RD.STRENGTH) AS STRENGTH,
    SUM(RD.Count_90_100) AS Count_90_100,
    SUM(RD.Count_80_90) AS Count_80_90,
    SUM(RD.Count_70_80) AS Count_70_80,
    SUM(RD.Count_60_70) AS Count_60_70,
    SUM(RD.Count_50_60) AS Count_50_60,
    SUM(RD.Count_40_50) AS Count_40_50,
    SUM(RD.Count_0_39) AS Count_0_39,
    SUM(RD.Above_70) AS Above_70,
    SUM(RD.Below_70) AS Below_70,
    SUM(RD.APPEARED) AS APPEARED,
    SUM(RD.PASSED) AS PASSED,
    CAST(SUM(RD.PASSED) * 100.0 / NULLIF(SUM(RD.APPEARED), 0) AS DECIMAL(5,2)) AS [PASS%],

    -- 🔹 Use CLASS AVG from vTeacher_all_sec_per (already joined)
    AVG(RD.CLASS_AVG) AS [CLASS AVG],

    CAST(RANK() OVER (
        PARTITION BY RD.CLASS, RD.Year, UPPER(LTRIM(RTRIM(RD.SUBJECT)))
        ORDER BY AVG(RD.CLASS_AVG) DESC
    ) AS INT) AS Position,

    COUNT(*) OVER (PARTITION BY RD.CLASS, RD.Year, UPPER(LTRIM(RTRIM(RD.SUBJECT)))) AS TOTAL_POSITIONS,
    AVG(RD.WL) AS WL,

    (
        SELECT STRING_AGG(SCHOOL, '-')
        FROM (
            SELECT DISTINCT SCHOOL
            FROM TR_ALL
            WHERE EID = RD.EID AND Year = RD.Year
        ) AS SchoolList
    ) AS [SCHOOL-MERGE],

    (
        SELECT STRING_AGG(abbreviation, '-')
        FROM (
            SELECT DISTINCT CS.abbreviation
            FROM TR_ALL T
            INNER JOIN CorrectSubjects CS
                ON UPPER(LTRIM(RTRIM(T.SUBJECT))) = UPPER(LTRIM(RTRIM(CS.subject)))
            WHERE T.EID = RD.EID AND T.Year = RD.Year
        ) AS SubjectList
    ) AS SUBJECT_MERGE

FROM RankedData RD
GROUP BY 
    RD.EID, 
    RD.NAME, 
    RD.SCHOOL, 
    RD.EXAMTYPE, 
    RD.SUBJECT, 
    RD.CLASS, 
    RD.Year;

GO

-- View: [dbo].[TR_ALL_SECTIONS_POS_old] (Object ID: 686625489)
-- Created: 2025-05-27T10:59:20.280 | Modified: 2025-10-21T11:25:05.100
CREATE VIEW [dbo].[TR_ALL_SECTIONS_POS_old] AS
WITH RankedData AS (
    SELECT
        EID,
        NAME,
        SCHOOL,
        EXAMTYPE,
        SUBJECT,
        CLASS,
        SECTION,
        Year,
        CATEGROY,
        STRENGTH,
        Count_90_100,
        Count_80_90,
        Count_70_80,
        Count_60_70,
        Count_50_60,
        Count_40_50,
        Count_0_39,
        APPEARED,
        PASSED,
        [PASS%] AS PASS_PERCENT,
        [CLASS AVG] AS CLASS_AVG,
        (ISNULL(Count_90_100, 0) + ISNULL(Count_80_90, 0) + ISNULL(Count_70_80, 0)) AS Above_70,
        (ISNULL(Count_60_70, 0) + ISNULL(Count_50_60, 0) + ISNULL(Count_40_50, 0) + ISNULL(Count_0_39, 0)) AS Below_70,
        COUNT(*) OVER (PARTITION BY EID, Year) AS WL,
        COUNT(*) OVER (PARTITION BY CLASS, Year, UPPER(LTRIM(RTRIM(SUBJECT)))) AS TOTAL_POSITIONS,
        CAST(RANK() OVER (
            PARTITION BY CLASS, Year, UPPER(LTRIM(RTRIM(SUBJECT)))
            ORDER BY [CLASS AVG] DESC
        ) AS INT) AS Position
    FROM TR_ALL
    WHERE CATEGROY = 'ALL'
)

SELECT
    EID,
    NAME,
    SCHOOL,
    EXAMTYPE,
    SUBJECT,
    CLASS,
    'ALL' AS SECTION,
    Year,
    'ALL SEC CAT' AS CATEGROY,
    SUM(STRENGTH) AS STRENGTH,
    SUM(Count_90_100) AS Count_90_100,
    SUM(Count_80_90) AS Count_80_90,
    SUM(Count_70_80) AS Count_70_80,
    SUM(Count_60_70) AS Count_60_70,
    SUM(Count_50_60) AS Count_50_60,
    SUM(Count_40_50) AS Count_40_50,
    SUM(Count_0_39) AS Count_0_39,
    SUM(Above_70) AS Above_70,
    SUM(Below_70) AS Below_70,
    SUM(APPEARED) AS APPEARED,
    SUM(PASSED) AS PASSED,
    CAST(SUM(PASSED) * 100.0 / NULLIF(SUM(APPEARED), 0) AS DECIMAL(5,2)) AS [PASS%],
    AVG(CLASS_AVG) AS [CLASS AVG],
    CAST(RANK() OVER (
        PARTITION BY CLASS, Year, UPPER(LTRIM(RTRIM(SUBJECT)))
        ORDER BY AVG(CLASS_AVG) DESC
    ) AS INT) AS Position,
    COUNT(*) OVER (PARTITION BY CLASS, Year, UPPER(LTRIM(RTRIM(SUBJECT)))) AS TOTAL_POSITIONS,
    AVG(WL) AS WL,
    (
        SELECT STRING_AGG(SCHOOL, '-') 
        FROM (
            SELECT DISTINCT SCHOOL 
            FROM TR_ALL 
            WHERE EID = RD.EID AND Year = RD.Year
        ) AS SchoolList
    ) AS [SCHOOL-MERGE],
    (
        SELECT STRING_AGG(abbreviation, '-') 
        FROM (
            SELECT DISTINCT CS.abbreviation
            FROM TR_ALL T
            INNER JOIN CorrectSubjects CS 
                ON UPPER(LTRIM(RTRIM(T.SUBJECT))) = UPPER(LTRIM(RTRIM(CS.subject)))
            WHERE T.EID = RD.EID AND T.Year = RD.Year
        ) AS SubjectList
    ) AS SUBJECT_MERGE
FROM RankedData RD
GROUP BY EID, NAME, SCHOOL, EXAMTYPE, SUBJECT, CLASS, Year;

GO

-- View: [dbo].[VW_TEACHER_SUMMARY_MNWB] (Object ID: 1742629251)
-- Created: 2025-06-10T20:07:17.967 | Modified: 2025-06-10T20:07:17.967
CREATE VIEW [dbo].[VW_TEACHER_SUMMARY_MNWB] AS
WITH DistinctSubjects AS (
    SELECT 
        EID,
        NAME,
        SCHOOL,
        CASE 
            WHEN CLASS IN ('9','10','11','12') THEN 'BOARD'
            WHEN CLASS IN ('6','7','8') THEN 'MIDDLE'
        END AS CATEGROY,
        CASE SUBJECT
             WHEN 'Mathematics' THEN 'MTH'
            WHEN 'GENERAL Science' THEN 'SCI'
            WHEN 'English' THEN 'ENG'
            WHEN 'Computer Science' THEN 'CS'
            WHEN 'Biology' THEN 'BIO'
            WHEN 'Physics' THEN 'PHY'
            WHEN 'Chemistry' THEN 'CHM'
            WHEN 'PAKISTAN STUDIES' THEN 'PST'
            WHEN 'ISLAMIYAT' THEN 'ISL'
			WHEN 'ISLAMIC EDUCATION' THEN 'ISE'
            WHEN 'TRANSLATION OF THE HOLY QURAN' THEN 'TJQ'
            WHEN 'ARTS' THEN 'ART'
			WHEN 'SOCIAL STUDIES' THEN 'SST'
			WHEN 'URDU' THEN 'URD'
            ELSE SUBJECT
        END AS SUBJECT_ABBR
    FROM TR_ALL_DEDUCTED
    WHERE CLASS IN ('6','7','8','9','10','11','12')
      AND SCHOOL = 'MNWB'
    GROUP BY EID, NAME, SCHOOL, CLASS, SUBJECT
),
SubjectAgg AS (
    SELECT 
        EID,
        CATEGROY,
        STRING_AGG(SUBJECT_ABBR, '-' ) AS SUBJECTS
    FROM (
        SELECT DISTINCT EID, CATEGROY, SUBJECT_ABBR
        FROM DistinctSubjects
    ) AS UniqueSubjects
    GROUP BY EID, CATEGROY
),
BaseData AS (
    SELECT
        EID,
        NAME,
        SCHOOL,
        SUBJECT,
        CLASS,
        STRENGTH,
        APPEARED,
        PASSED,
        FAIL,
        [CLASS AVG],
        DEDUCTION,
        CASE 
            WHEN CLASS IN ('9','10','11','12') THEN 'BOARD'
            WHEN CLASS IN ('6','7','8') THEN 'MIDDLE'
        END AS CATEGROY
    FROM TR_ALL_DEDUCTED
    WHERE CLASS IN ('6','7','8','9','10','11','12')
      AND SCHOOL = 'MNWB'
)
SELECT
    A.EID,
    A.NAME,
    A.SCHOOL,
    S.SUBJECTS AS SUBJECT,
    A.CATEGROY,
    SUM(A.STRENGTH) AS STRENGTH,
    SUM(A.APPEARED) AS APPEARED,
    SUM(A.PASSED) AS PASSED,
    SUM(A.FAIL) AS FAIL,
    AVG(A.[CLASS AVG]) AS [CLASS AVG],
    SUM(A.DEDUCTION) AS DEDUCTION
FROM BaseData A
JOIN SubjectAgg S ON A.EID = S.EID AND A.CATEGROY = S.CATEGROY
GROUP BY A.EID, A.NAME, A.SCHOOL, A.CATEGROY, S.SUBJECTS;

GO

-- View: [dbo].[VW_Tr_all_Aggregated_Summary] (Object ID: 384720423)
-- Created: 2025-09-22T13:12:03.700 | Modified: 2025-09-22T13:12:03.700
CREATE VIEW [dbo].[VW_Tr_all_Aggregated_Summary] AS
WITH EID_AGG AS (
  SELECT
    SCHOOL,
    EID,
    NAME,
    SUBJECT,
    'ALL' AS Year,
    'ALL' AS CLASS,
    SUM(APPEARED) AS APPEARED,
    SUM(PASSED) AS PASSED,
    AVG([CLASS AVG]) AS [CLASS AVG],
    SUM(Count_90_100) AS Total_Above_90,
    SUM(Count_0_39) AS Total_Below_40
  FROM Tr_all
  WHERE
    CLASS IN (9, 10, 11, 12) AND Year IN (22, 23, 24, 25)
  GROUP BY
    SCHOOL,
    EID,
    NAME,
    SUBJECT
)
SELECT
  SCHOOL,
  EID,
  NAME,
  SUBJECT,
  CAST(Year AS VARCHAR(10)) AS Year,
  CAST(CLASS AS VARCHAR(10)) AS CLASS,
  APPEARED,
  PASSED,
  [CLASS AVG],
  CAST(ROUND((CAST(Count_90_100 AS FLOAT) / APPEARED) * 100, 2) AS DECIMAL(5, 2)) AS [Above 90 %],
  CAST(ROUND((CAST(Count_0_39 AS FLOAT) / APPEARED) * 100, 2) AS DECIMAL(5, 2)) AS [Below 40 %]
FROM Tr_all
WHERE
  CLASS IN (9, 10, 11, 12) AND Year IN (22, 23, 24, 25)
UNION ALL
SELECT
  SCHOOL,
  EID,
  NAME,
  SUBJECT,
  Year,
  CLASS,
  APPEARED,
  PASSED,
  [CLASS AVG],
  CAST(ROUND((CAST(Total_Above_90 AS FLOAT) / APPEARED) * 100, 2) AS DECIMAL(5, 2)) AS [Above 90 %],
  CAST(ROUND((CAST(Total_Below_40 AS FLOAT) / APPEARED) * 100, 2) AS DECIMAL(5, 2)) AS [Below 40 %]
FROM EID_AGG;

GO

-- View: [dbo].[V_SCHOOL_STDUENTS_INTERNAL_ERROR_CHK] (Object ID: 521768916)
-- Created: 2025-11-24T08:03:21.927 | Modified: 2025-11-24T08:03:21.927
-- View to summarize data quality errors, grouped by School and Class.
-- It reports the COUNT of errors for each validation category within each School/Class segment.

CREATE VIEW [dbo].[V_SCHOOL_STDUENTS_INTERNAL_ERROR_CHK] AS
SELECT
    SCHOOL,
    CLASS,
    -- Counting Missing Data for SCHOOL
    SUM(CASE WHEN ValidationStatus LIKE '%SCHOOL%' THEN 1 ELSE 0 END) AS SCHOOL_Errors,

    -- Counting Missing Data and Invalid GROUPs
    SUM(CASE WHEN ValidationStatus LIKE '%GROUP%' THEN 1 ELSE 0 END) AS GROUP_Errors,
    
    -- Counting Missing Data for SMSNO
    SUM(CASE WHEN ValidationStatus LIKE '%SMSNO%' THEN 1 ELSE 0 END) AS SMSNO_Errors,
    
    -- Counting Missing Data for ROLLNO
    SUM(CASE WHEN ValidationStatus LIKE '%ROLLNO%' THEN 1 ELSE 0 END) AS ROLLNO_Errors,
    
    -- Counting Missing Data for STUDENT
    SUM(CASE WHEN ValidationStatus LIKE '%STUDENT%' AND ValidationStatus LIKE 'Missing Data:%' THEN 1 ELSE 0 END) AS STUDENT_Errors,
    
    -- Counting Missing Data for FATHER
    SUM(CASE WHEN ValidationStatus LIKE '%FATHER%' AND ValidationStatus LIKE 'Missing Data:%' THEN 1 ELSE 0 END) AS FATHER_Errors,
    
    -- Counting ALL CLASS-related errors: Missing, Invalid Class Value (6-12), and Group Mismatch
    SUM(CASE 
        WHEN ValidationStatus LIKE '%CLASS%' OR ValidationStatus LIKE '%Group/Class Error%' THEN 1 
        ELSE 0 
    END) AS CLASS_Errors, 
    
    -- Counting Missing Data for SECTION
    SUM(CASE WHEN ValidationStatus LIKE '%SECTION%' THEN 1 ELSE 0 END) AS SECTION_Errors,
    
    -- Counting ALL CATEGORY-related errors: Missing and Invalid Value (B, DS, S)
    SUM(CASE WHEN ValidationStatus LIKE '%CATEGORY%' THEN 1 ELSE 0 END) AS CATEGORY_Errors, 
    
    -- Counting Missing Data for YEAR
    SUM(CASE WHEN ValidationStatus LIKE '%YEAR%' AND ValidationStatus LIKE 'Missing Data:%' THEN 1 ELSE 0 END) AS YEAR_Errors,
    
    -- Counting Missing Data for HOUSE
    SUM(CASE WHEN ValidationStatus LIKE '%HOUSE%' THEN 1 ELSE 0 END) AS HOUSE_Errors,
    
    -- Total Errors in this specific School/Class combination
    COUNT(CASE WHEN ValidationStatus != 'OK' THEN 1 END) AS Total_Errors_in_Group
    
FROM 
    V_STUDENT_DATA_QUALITY_CHECK_INTERNAL
WHERE 
    ValidationStatus != 'OK' -- Crucial filter: Only process rows that have errors
GROUP BY
    SCHOOL,
    CLASS
;

GO

-- View: [dbo].[V_STUDENT_DATA_QUALITY_CHECK_INTERNAL] (Object ID: 505768859)
-- Created: 2025-11-24T07:54:45.170 | Modified: 2025-11-24T07:54:45.170
-- View to check data integrity and consistency in STUDENTS_ROLL_INTERNAL_EXAM.
-- It flags records that violate the expected GROUP/CLASS structure or have missing required data.
-- This view should be run using 'SELECT * FROM V_STUDENT_DATA_QUALITY_CHECK;' 
-- or 'SELECT * FROM V_STUDENT_DATA_QUALITY_CHECK WHERE ValidationStatus != 'OK';'

CREATE VIEW [dbo].[V_STUDENT_DATA_QUALITY_CHECK_INTERNAL] AS
SELECT
    ID,
    SCHOOL,
    [GROUP], -- Quoted for safety
    CLASS,
    SECTION,
    CATEGORY,
    [YEAR],  -- Quoted for safety
    STUDENT,
    -- Flagging Validation/Error Status
    CASE
        -- NEW CHECK 1: General CLASS Value Range (Must be 6-12)
        WHEN CLASS IS NOT NULL AND CLASS NOT IN (6, 7, 8, 9, 10, 11, 12) THEN 'Group/Class Error: CLASS must be 6-12'

        -- CHECK 2: Group/Class Consistency (Original Rules)
        WHEN [GROUP] = 'GENERAL SCIENCE' AND CLASS NOT IN (6, 7, 8, 9, 10, 11, 12) THEN 'Group/Class Error: GS Class Invalid'
        WHEN [GROUP] IN ('PRE-ENGINEERING', 'PRE-MEDICAL') AND CLASS NOT IN (9, 10, 11, 12) THEN 'Group/Class Error: Pre-Group Class Invalid'
        WHEN [GROUP] NOT IN ('GENERAL SCIENCE', 'PRE-ENGINEERING', 'PRE-MEDICAL') THEN 'Group/Class Error: Invalid Group'

        -- NEW CHECK 3: Category Consistency (Must be B, DS, S)
        WHEN CATEGORY IS NOT NULL AND CATEGORY NOT IN ('B', 'DS', 'S') THEN 'Data Error: Invalid CATEGORY Value (Must be B, DS, or S)'
        
        -- CHECK 4: Missing Data (NULL or empty string checks for required columns)
        WHEN SCHOOL IS NULL OR LTRIM(RTRIM(SCHOOL)) = '' THEN 'Missing Data: SCHOOL'
        WHEN [GROUP] IS NULL OR LTRIM(RTRIM([GROUP])) = '' THEN 'Missing Data: GROUP'
        WHEN SMSNO IS NULL OR LTRIM(RTRIM(SMSNO)) = '' THEN 'Missing Data: SMSNO'
        WHEN ROLLNO IS NULL OR LTRIM(RTRIM(ROLLNO)) = '' THEN 'Missing Data: ROLLNO'
        WHEN STUDENT IS NULL OR LTRIM(RTRIM(STUDENT)) = '' THEN 'Missing Data: STUDENT Name'
        WHEN FATHER IS NULL OR LTRIM(RTRIM(FATHER)) = '' THEN 'Missing Data: FATHER Name'
        WHEN CLASS IS NULL THEN 'Missing Data: CLASS'
        WHEN SECTION IS NULL OR LTRIM(RTRIM(SECTION)) = '' THEN 'Missing Data: SECTION'
        WHEN CATEGORY IS NULL OR LTRIM(RTRIM(CATEGORY)) = '' THEN 'Missing Data: CATEGORY'
        WHEN [YEAR] IS NULL THEN 'Missing Data: YEAR'
        WHEN HOUSE IS NULL OR LTRIM(RTRIM(HOUSE)) = '' THEN 'Missing Data: HOUSE'
        
        ELSE 'OK'
    END AS ValidationStatus
FROM
    STUDENTS_ROLL_INTERNAL_EXAM
-- The WHERE clause filters the view to show rows with errors, plus all "OK" rows.
-- If you only want to see error rows, remove 'OR 1 = 1'.
WHERE
    (
        -- Group/Class Checks
        CLASS IS NOT NULL AND CLASS NOT IN (6, 7, 8, 9, 10, 11, 12)
        OR ([GROUP] = 'GENERAL SCIENCE' AND CLASS NOT IN (6, 7, 8, 9, 10, 11, 12))
        OR ([GROUP] IN ('PRE-ENGINEERING', 'PRE-MEDICAL') AND CLASS NOT IN (9, 10, 11, 12))
        OR [GROUP] NOT IN ('GENERAL SCIENCE', 'PRE-ENGINEERING', 'PRE-MEDICAL')

        -- Category Check
        OR (CATEGORY IS NOT NULL AND CATEGORY NOT IN ('B', 'DS', 'S'))
        
        -- Missing Data Checks (original required columns)
        OR SCHOOL IS NULL OR LTRIM(RTRIM(SCHOOL)) = ''
        OR [GROUP] IS NULL OR LTRIM(RTRIM([GROUP])) = ''
        OR SMSNO IS NULL OR LTRIM(RTRIM(SMSNO)) = ''
        OR ROLLNO IS NULL OR LTRIM(RTRIM(ROLLNO)) = ''
        OR STUDENT IS NULL OR LTRIM(RTRIM(STUDENT)) = ''
        OR FATHER IS NULL OR LTRIM(RTRIM(FATHER)) = ''
        OR CLASS IS NULL
        OR SECTION IS NULL OR LTRIM(RTRIM(SECTION)) = ''
        OR CATEGORY IS NULL OR LTRIM(RTRIM(CATEGORY)) = ''
        OR [YEAR] IS NULL
        OR HOUSE IS NULL OR LTRIM(RTRIM(HOUSE)) = ''
    )
    OR 1 = 1
;

GO

-- View: [dbo].[c6] (Object ID: 811149935)
-- Created: 2025-06-22T12:33:40.500 | Modified: 2025-06-22T12:33:40.500
CREATE VIEW [dbo].[c6] AS
WITH BaseData AS (
    SELECT
        SCHOOL,
        STUDENT,
        FATHER,
        CLASS,
        SECTION,
        YEAR,
        ROLLNO,
        SUBJECT,
        OBTAINED
    FROM students_result_total
    WHERE SUBJECT <> 'TOTAL'
),
Pivoted AS (
    SELECT
        SCHOOL,
        STUDENT,
        FATHER,
        CLASS,
        SECTION,
        YEAR,
        ROLLNO,
        [URDU],
        [ENGLISH],
        [ISLAMIYAT],
        [PAKISTAN STUDIES],
        [MATHEMATICS],
        [PHYSICS],
        [CHEMISTRY],
        [BIOLOGY],
        [TRANSLATION OF THE HOLY QURAN],
        [ISLAMIC EDUCATION],
        [COMPUTER SCIENCE],
        [SOCIAL STUDIES],
        [GENERAL SCIENCE],
        [ARTS]
    FROM BaseData
    PIVOT (
        MAX(OBTAINED)
        FOR SUBJECT IN (
            [URDU],
            [ENGLISH],
            [ISLAMIYAT],
            [PAKISTAN STUDIES],
            [MATHEMATICS],
            [PHYSICS],
            [CHEMISTRY],
            [BIOLOGY],
            [TRANSLATION OF THE HOLY QURAN],
            [ISLAMIC EDUCATION],
            [COMPUTER SCIENCE],
            [SOCIAL STUDIES],
            [GENERAL SCIENCE],
            [ARTS]
        )
    ) AS PivotTable
),
StudentTotalMarks AS (
    SELECT
        STUDENT,
        CLASS,
        SECTION,
        YEAR,
        MAX(TOTAL) AS TOTAL_MARKS
    FROM students_result_total
    WHERE SUBJECT = 'TOTAL'
    GROUP BY STUDENT, CLASS, SECTION, YEAR
),
WithTotals AS (
    SELECT 
        pvt.*,
        ISNULL([URDU], 0) + ISNULL([ENGLISH], 0) + ISNULL([ISLAMIYAT], 0) +
        ISNULL([PAKISTAN STUDIES], 0) + ISNULL([MATHEMATICS], 0) +
        ISNULL([PHYSICS], 0) + ISNULL([CHEMISTRY], 0) + ISNULL([BIOLOGY], 0) +
        ISNULL([TRANSLATION OF THE HOLY QURAN], 0) + ISNULL([ISLAMIC EDUCATION], 0) +
        ISNULL([COMPUTER SCIENCE], 0) + ISNULL([SOCIAL STUDIES], 0) +
        ISNULL([GENERAL SCIENCE], 0) + ISNULL([ARTS], 0) AS TOTAL_OBTAINED,
        tm.TOTAL_MARKS,
        ROUND((
            ISNULL([URDU], 0) + ISNULL([ENGLISH], 0) + ISNULL([ISLAMIYAT], 0) +
            ISNULL([PAKISTAN STUDIES], 0) + ISNULL([MATHEMATICS], 0) +
            ISNULL([PHYSICS], 0) + ISNULL([CHEMISTRY], 0) + ISNULL([BIOLOGY], 0) +
            ISNULL([TRANSLATION OF THE HOLY QURAN], 0) + ISNULL([ISLAMIC EDUCATION], 0) +
            ISNULL([COMPUTER SCIENCE], 0) + ISNULL([SOCIAL STUDIES], 0) +
            ISNULL([GENERAL SCIENCE], 0) + ISNULL([ARTS], 0)
        ) * 100.0 / NULLIF(tm.TOTAL_MARKS, 0), 2) AS PERCENTAGE
    FROM Pivoted pvt
    JOIN StudentTotalMarks tm
      ON tm.STUDENT = pvt.STUDENT
     AND tm.CLASS = pvt.CLASS
     AND tm.SECTION = pvt.SECTION
     AND tm.YEAR = pvt.YEAR
)
SELECT *,
    CASE
        WHEN EXISTS (
            SELECT 1 FROM students_result_total st
            WHERE st.STUDENT = wt.STUDENT
              AND st.CLASS = wt.CLASS
              AND st.SECTION = wt.SECTION
              AND st.YEAR = wt.YEAR
              AND st.STATUS = 'FAIL'
        ) THEN 'FAIL'
        ELSE 'PASS'
    END AS FINAL_STATUS
FROM WithTotals AS wt;

GO

-- View: [dbo].[teachers_exam_data_errors_v2] (Object ID: 1321771766)
-- Created: 2025-12-01T05:05:54.757 | Modified: 2025-12-01T05:05:54.757
-- VIEW to check data quality and consistency in the TEACHERS_INTERNAL_EXAM table
-- based on reference data in SUBJECT_GORUP_YEAR_MARKS_26 and STUDENTS_ROLL_INTERNAL_EXAM.

CREATE VIEW [dbo].[teachers_exam_data_errors_v2] AS

-- -----------------------------------------------------------
-- PART 1: Find NULL or Empty Column Data (Error 1)
-- Identifies records with NULL or empty values in critical columns.
-- -----------------------------------------------------------
SELECT
    ID,
    EID,
    NAME,
    CLASS,
    SECTION,
    SUBJECT,
    SCHOOL,
    YEAR,
    'Missing Data (NULL/Empty)' AS Error_Type,
    CASE
        WHEN NAME IS NULL OR NAME = '' THEN 'Missing Teacher Name'
        WHEN CLASS IS NULL OR CLASS = '' THEN 'Missing Class'
        WHEN SECTION IS NULL OR SECTION = '' THEN 'Missing Section'
        WHEN SUBJECT IS NULL OR SUBJECT = '' THEN 'Missing Subject'
        WHEN SCHOOL IS NULL OR SCHOOL = '' THEN 'Missing School'
        WHEN YEAR IS NULL OR YEAR = '' THEN 'Missing Year'
        WHEN EXAM IS NULL OR EXAM = '' THEN 'Missing Exam Type'
        ELSE 'Unknown Data Error' -- Should not be hit if criteria are correct
    END AS Error_Detail
FROM
    TEACHERS_INTERNAL_EXAM
WHERE
    NAME IS NULL OR NAME = ''
    OR CLASS IS NULL OR CLASS = ''
    OR SECTION IS NULL OR SECTION = ''
    OR SUBJECT IS NULL OR SUBJECT = ''
    OR SCHOOL IS NULL OR SCHOOL = ''
    OR YEAR IS NULL OR YEAR = ''
    OR EXAM IS NULL OR EXAM = ''

UNION ALL

-- -----------------------------------------------------------
-- PART 2: Invalid Subject Spelling or Invalid Subject-Class Combination (Error 2)
-- Checks if the SUBJECT for a given CLASS in TEACHERS_INTERNAL_EXAM exists
-- in the SUBJECT_GORUP_YEAR_MARKS_26 reference table.
-- -----------------------------------------------------------
SELECT
    TIE.ID,
    TIE.EID,
    TIE.NAME,
    TIE.CLASS,
    TIE.SECTION,
    TIE.SUBJECT,
    TIE.SCHOOL,
    TIE.YEAR,
    'Invalid Subject/Class' AS Error_Type,
    'The subject is either misspelled or not registered for this class in the marks table.' AS Error_Detail
FROM
    TEACHERS_INTERNAL_EXAM AS TIE
LEFT JOIN
    SUBJECT_GORUP_YEAR_MARKS_26 AS SGYM
    ON TIE.CLASS = SGYM.CLASS AND TIE.SUBJECT = SGYM.SUBJECT
WHERE
    SGYM.CLASS IS NULL -- No match found in the reference table
    AND TIE.SUBJECT IS NOT NULL AND TIE.SUBJECT != '' -- Exclude errors already found in Part 1

UNION ALL

-- -----------------------------------------------------------
-- PART 3: Missing Subject Allocation for Class/Section/Group (Error 3)
-- 1. Finds the unique GROUP for each CLASS/SECTION from the STUDENTS table.
-- 2. Compares the required SUBJECTs (based on that GROUP/CLASS) against the actual
--    SUBJECTs taught in TEACHERS_INTERNAL_EXAM.
-- -----------------------------------------------------------
SELECT
    TIE.ID,
    TIE.EID,
    TIE.NAME,
    TIE.CLASS,
    TIE.SECTION,
    TIE.SUBJECT,
    TIE.SCHOOL,
    TIE.YEAR,
    'Mismatched Subject Allocation' AS Error_Type,
    'The subject is not allocated to this specific Class/Section/Group combination.' AS Error_Detail
FROM
    TEACHERS_INTERNAL_EXAM AS TIE
LEFT JOIN
    (
        -- Subquery to link the teacher record to the correct GROUP and valid SUBJECT/CLASS combination
        SELECT DISTINCT
            SRI.CLASS,    -- Corrected from SRIE.CLASS to SRI.CLASS
            SRI.SECTION,  -- Corrected from SRIE.SECTION to SRI.SECTION
            SRI.[GROUP],  -- Corrected from SRIE.[GROUP] to SRI.[GROUP]
            SGYM.SUBJECT -- Valid Subject for that GROUP and CLASS
        FROM
            STUDENTS_ROLL_INTERNAL_EXAM AS SRI
        INNER JOIN
            SUBJECT_GORUP_YEAR_MARKS_26 AS SGYM
            ON SGYM.CLASS = SRI.CLASS AND SGYM.[GROUP] = SRI.[GROUP]
    ) AS ValidAllocations
    ON TIE.CLASS = ValidAllocations.CLASS
    AND TIE.SECTION = ValidAllocations.SECTION
    AND TIE.SUBJECT = ValidAllocations.SUBJECT
WHERE
    ValidAllocations.CLASS IS NULL -- A valid allocation was not found for the teacher's record
    AND TIE.SUBJECT IS NOT NULL AND TIE.SUBJECT != '' -- Exclude errors already found in Part 1

UNION ALL

-- -----------------------------------------------------------
-- PART 4: Missing Required Class Allocation (Error 4)
-- Checks if any required CLASS for a SCHOOL is entirely missing from the TIE table.
-- Required classes are 6-12 (unless school is MNKB, MNKG, TNSB, TNSG, in which case 6-8).
-- -----------------------------------------------------------
SELECT
    NULL AS ID,        -- The record is missing, so no ID exists
    NULL AS EID,
    NULL AS NAME,
    E.CLASS,           -- The missing class
    NULL AS SECTION,
    NULL AS SUBJECT,
    E.SCHOOL,
    NULL AS YEAR,
    'Missing Class Allocation' AS Error_Type,
    'The required class ' + E.CLASS + ' is missing entirely for school ' + E.SCHOOL + '.' AS Error_Detail
FROM
    (
        -- E: Expected Class Allocations (Generate all required (SCHOOL, CLASS) pairs)
        SELECT
            T.SCHOOL,
            RC.CLASS
        FROM
            (SELECT DISTINCT SCHOOL FROM TEACHERS_INTERNAL_EXAM) AS T -- Get all unique schools present in the data
        CROSS JOIN
            (
                -- Define all possible required classes (6-12)
                SELECT '6' AS CLASS UNION ALL SELECT '7' UNION ALL SELECT '8' UNION ALL
                SELECT '9' UNION ALL SELECT '10' UNION ALL SELECT '11' UNION ALL SELECT '12'
            ) AS RC
        WHERE
            -- Rule 1: Always include classes 6, 7, 8
            RC.CLASS IN ('6', '7', '8')
            OR (
                -- Rule 2: Only include classes 9, 10, 11, 12 if the school is NOT a special school
                RC.CLASS IN ('9', '10', '11', '12')
                AND T.SCHOOL NOT IN ('MNKB', 'MNKG', 'TNSB', 'TNSG')
            )
    ) AS E -- E is the EXPECTED list of (SCHOOL, CLASS) combinations
LEFT JOIN
    (SELECT DISTINCT SCHOOL, CLASS FROM TEACHERS_INTERNAL_EXAM) AS A -- A is the ACTUAL list of (SCHOOL, CLASS) combinations
    ON E.SCHOOL = A.SCHOOL AND E.CLASS = A.CLASS
WHERE
    A.SCHOOL IS NULL; -- The required combination (E) is missing from the actual data (A)

GO

-- View: [dbo].[vTHEORY] (Object ID: 1719677174)
-- Created: 2025-07-26T10:22:20.973 | Modified: 2025-07-26T10:22:20.973
CREATE VIEW [dbo].[vTHEORY] AS
SELECT 
    P.SUBJECT,
    
    -- OBTAINED = Marks.Obtained - Prac.Obtained
    (M.OBTAINED - P.OBTAINED) AS OBTAINED,

    -- TOTAL = Marks.Total - Prac.Total
    (M.TOTAL - P.TOTAL) AS TOTAL,

    -- Percentage Calculation
    CAST(ROUND(
        CAST((M.OBTAINED - P.OBTAINED) AS FLOAT) / NULLIF((M.TOTAL - P.TOTAL), 0) * 100, 2
    ) AS FLOAT) AS [%],

    -- Grade Assignment
    CASE 
        WHEN (M.OBTAINED - P.OBTAINED) * 100.0 / NULLIF((M.TOTAL - P.TOTAL), 0) >= 90 THEN 'A+'
        WHEN (M.OBTAINED - P.OBTAINED) * 100.0 / NULLIF((M.TOTAL - P.TOTAL), 0) >= 85 THEN 'A'
        WHEN (M.OBTAINED - P.OBTAINED) * 100.0 / NULLIF((M.TOTAL - P.TOTAL), 0) >= 80 THEN 'B+'
        WHEN (M.OBTAINED - P.OBTAINED) * 100.0 / NULLIF((M.TOTAL - P.TOTAL), 0) >= 75 THEN 'B'
        WHEN (M.OBTAINED - P.OBTAINED) * 100.0 / NULLIF((M.TOTAL - P.TOTAL), 0) >= 70 THEN 'C+'
        WHEN (M.OBTAINED - P.OBTAINED) * 100.0 / NULLIF((M.TOTAL - P.TOTAL), 0) >= 60 THEN 'C'
        WHEN (M.OBTAINED - P.OBTAINED) * 100.0 / NULLIF((M.TOTAL - P.TOTAL), 0) >= 50 THEN 'D+'
        WHEN (M.OBTAINED - P.OBTAINED) * 100.0 / NULLIF((M.TOTAL - P.TOTAL), 0) >= 45 THEN 'D'
        WHEN (M.OBTAINED - P.OBTAINED) * 100.0 / NULLIF((M.TOTAL - P.TOTAL), 0) >= 33 THEN 'E'
        ELSE 'F'
    END AS GRADE,

    -- PASS / FAIL Status
    CASE 
        WHEN (M.OBTAINED - P.OBTAINED) * 100.0 / NULLIF((M.TOTAL - P.TOTAL), 0) > 32 THEN 'PASS'
        ELSE 'FAIL'
    END AS STATUS,

    P.ROLLNO,
    P.CLASS,
    P.YEAR,
    'ANNUAL-THEORY' AS EXAMTYPE
FROM dbo.MARKS M
JOIN dbo.PRAC P
    ON M.ROLLNO = P.ROLLNO
   AND M.CLASS = P.CLASS
   AND M.YEAR = P.YEAR
   AND M.SUBJECT = P.SUBJECT;

GO

-- View: [dbo].[vTeacher_all_sec_per] (Object ID: 269244014)
-- Created: 2025-10-21T11:19:12.510 | Modified: 2025-10-21T11:19:12.510
CREATE VIEW [dbo].[vTeacher_all_sec_per] AS
SELECT
    [EID],
    [NAME],
    [SCHOOL],
    [CLASS],
    [YEAR],
    [SUBJECT],
    SUM([SumObtained]) AS SumObtained,
    SUM([SumTotal]) AS SumTotal,
    CAST(
        ROUND(
            (SUM(CAST([SumObtained] AS FLOAT)) / NULLIF(SUM(CAST([SumTotal] AS FLOAT)), 0)) * 100,
            2
        ) AS DECIMAL(5,2)
    ) AS [%]
FROM vTeacher_sum_per
GROUP BY 
    [EID],
    [NAME],
    [SCHOOL],
    [CLASS],
    [YEAR],
    [SUBJECT];

GO

-- View: [dbo].[vTeacher_sum_per] (Object ID: 253243957)
-- Created: 2025-10-21T10:36:39.400 | Modified: 2025-10-21T10:36:39.400
CREATE VIEW [dbo].[vTeacher_sum_per] AS
SELECT
    t.EID,
    t.NAME,
    t.SCHOOL,
    t.CLASS,
    t.SECTION,
    t.YEAR,
    t.SUBJECT,
    SUM(m.OBTAINED) AS SumObtained,
    SUM(m.TOTAL) AS SumTotal,
    CAST(
        ROUND(
            (SUM(CAST(m.OBTAINED AS FLOAT)) / NULLIF(SUM(CAST(m.TOTAL AS FLOAT)), 0)) * 100, 
            2
        ) AS DECIMAL(5,2)
    ) AS [%]
FROM teahcers AS t
INNER JOIN students_roll AS s
    ON t.SCHOOL = s.SCHOOL
    AND t.CLASS = s.CLASS
    AND t.SECTION = s.SECTION
    AND t.YEAR = s.YEAR
INNER JOIN marks AS m
    ON s.ROLLNO = m.ROLLNO
    AND s.CLASS = m.CLASS
    AND s.YEAR = m.YEAR
    AND t.SUBJECT = m.SUBJECT
GROUP BY 
    t.EID,
    t.NAME,
    t.SCHOOL,
    t.CLASS,
    t.SECTION,
    t.YEAR,
    t.SUBJECT;

GO

-- View: [dbo].[vTeacher_sum_per_BOARD_MIDDLE] (Object ID: 365244356)
-- Created: 2025-10-23T13:57:06.273 | Modified: 2025-10-23T13:57:06.273
CREATE VIEW [dbo].[vTeacher_sum_per_BOARD_MIDDLE] AS
SELECT
    EID,
    NAME,
    SCHOOL,
    CASE 
        WHEN CLASS IN (9, 10, 11, 12) THEN 'BOARD'
        WHEN CLASS IN (6, 7, 8) THEN 'MIDDLE'
        ELSE 'OTHER'
    END AS CATEGROY,
    SUBJECT,
    SUM(SumObtained) AS SumObtained,
    SUM(SumTotal) AS SumTotal,
    ROUND(
        (SUM(SumObtained) * 100.0 / NULLIF(SUM(SumTotal), 0)), 2
    ) AS [%]
FROM vTeacher_sum_per
GROUP BY
    EID,
    NAME,
    SCHOOL,
    SUBJECT,
    CASE 
        WHEN CLASS IN (9, 10, 11, 12) THEN 'BOARD'
        WHEN CLASS IN (6, 7, 8) THEN 'MIDDLE'
        ELSE 'OTHER'
    END;

GO

-- View: [dbo].[vw_ALL_MISSING_TEACHERS] (Object ID: 523148909)
-- Created: 2025-06-18T11:35:33.103 | Modified: 2025-06-18T11:35:33.103
CREATE VIEW [dbo].[vw_ALL_MISSING_TEACHERS] AS
WITH RollGroups AS (
    SELECT DISTINCT
        SR.SCHOOL,
        SR.YEAR,
        SR.CLASS,
        SR.SECTION,
        SR.[GROUP]
    FROM students_roll AS SR
),
RequiredSubjects AS (
    SELECT 
        RG.SCHOOL,
        RG.YEAR,
        RG.CLASS,
        RG.SECTION,
        RG.[GROUP],
        SYM.SUBJECT
    FROM RollGroups AS RG
    JOIN SUBJECT_GROUP_YEAR_MARKS AS SYM
      ON RG.CLASS = SYM.CLASS
     AND RG.YEAR = SYM.YEAR
     AND RG.[GROUP] = SYM.[GROUP]
),
MissingAssignments AS (
    SELECT
        RS.SCHOOL,
        RS.YEAR,
        RS.CLASS,
        RS.SECTION,
        RS.[GROUP],
        RS.SUBJECT
    FROM RequiredSubjects RS
    LEFT JOIN teahcers T
      ON RS.SCHOOL = T.SCHOOL
     AND RS.YEAR = T.YEAR
     AND RS.CLASS = T.CLASS
     AND RS.SECTION = T.SECTION
     AND RS.SUBJECT = T.SUBJECT
    WHERE T.EID IS NULL
)
SELECT
    ROW_NUMBER() OVER (ORDER BY SCHOOL, YEAR, CLASS, SECTION, SUBJECT) AS SNO,
    SCHOOL,
    YEAR,
    CLASS,
    SECTION,
    [GROUP],
    SUBJECT
FROM MissingAssignments;

GO

-- View: [dbo].[vw_CLASS_YEAR_SUBJECT_AGGREGATE] (Object ID: 660197402)
-- Created: 2025-09-01T13:11:59.257 | Modified: 2025-09-01T13:11:59.257
CREATE VIEW [dbo].[vw_CLASS_YEAR_SUBJECT_AGGREGATE] AS
SELECT
    CLASS,
    YEAR,
    SUBJECT,
    SUM(OBTAINED) AS OBTAINED,
    SUM(TOTAL) AS TOTAL,
    CAST(ROUND(
        (SUM(CAST(OBTAINED AS FLOAT)) / NULLIF(SUM(NULLIF(TOTAL, 0)), 0)) * 100, 
        2
    ) AS DECIMAL(5, 2)) AS [%]
FROM
    vw_SCHOOL_SUBJECT_WISE_POS
GROUP BY
    CLASS,
    YEAR,
    SUBJECT;

GO

-- View: [dbo].[vw_CONSOLIDATED_ACCURATE] (Object ID: 1831677573)
-- Created: 2025-07-28T21:35:15.293 | Modified: 2026-05-19T23:31:53.603
CREATE VIEW [dbo].[vw_CONSOLIDATED_ACCURATE] AS
WITH FilteredSubjects AS (
    SELECT *
    FROM students_result_total
    WHERE SUBJECT <> 'TOTAL'
),
PivotedSubjects AS (
    SELECT
        SCHOOL,
        STUDENT,
        FATHER,
        CLASS,
        SECTION,
        [YEAR],
        SMSNO,
        ROLLNO,
        [GROUP],
        SUBJECT,
        OBTAINED,
        TOTAL,
        STATUS
    FROM FilteredSubjects
),
SubjectPivot AS (
    SELECT
        SCHOOL,
        STUDENT,
        FATHER,
        CLASS,
        SECTION,
        [YEAR],
        SMSNO,
        ROLLNO,
        [GROUP],
        [CHEMISTRY],
        [COMPUTER SCIENCE],
        [ENGLISH],
        [ISLAMIC EDUCATION],
        [ISLAMIYAT],
        [MATHEMATICS],
        [PAKISTAN STUDIES],
        [PHYSICS],
        [TRANSLATION OF THE HOLY QURAN],
        [URDU],
        [BIOLOGY],
        [SOCIAL STUDIES],
        [ARTS],
        [GENERAL SCIENCE] -- Added Subject Here
    FROM (
        SELECT 
            SCHOOL,
            STUDENT,
            FATHER,
            CLASS,
            SECTION,
            [YEAR],
            SMSNO,
            ROLLNO,
            [GROUP],
            SUBJECT,
            OBTAINED
        FROM PivotedSubjects
    ) AS SourceTable
    PIVOT (
        MAX(OBTAINED)
        FOR SUBJECT IN (
            [CHEMISTRY],
            [COMPUTER SCIENCE],
            [ENGLISH],
            [ISLAMIC EDUCATION],
            [ISLAMIYAT],
            [MATHEMATICS],
            [PAKISTAN STUDIES],
            [PHYSICS],
            [TRANSLATION OF THE HOLY QURAN],
            [URDU],
            [BIOLOGY],
            [SOCIAL STUDIES],
            [ARTS],
            [GENERAL SCIENCE] -- Added Subject Here
        )
    ) AS Pivoted
),
TotalScores AS (
    SELECT 
        S.*,
        ST.SUM_OBTAINED,
        ST.SUM_TOTAL,
        ROUND(CAST(ST.SUM_OBTAINED AS FLOAT) / NULLIF(ST.SUM_TOTAL, 0) * 100, 2) AS [%],
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM FilteredSubjects R
                WHERE R.STUDENT = S.STUDENT 
                    AND R.SCHOOL = S.SCHOOL 
                    AND R.CLASS = S.CLASS 
                    AND R.SECTION = S.SECTION 
                    AND R.YEAR = S.YEAR
                    AND R.SMSNO = S.SMSNO
                    AND R.ROLLNO = S.ROLLNO
                    AND R.STATUS = 'FAIL'
            ) THEN 'FAIL'
            ELSE 'PASS'
        END AS FINAL_STATUS,
        CASE 
            WHEN ROUND(CAST(ST.SUM_OBTAINED AS FLOAT) / NULLIF(ST.SUM_TOTAL, 0) * 100, 2) >= 90 THEN 'A+'
            WHEN ROUND(CAST(ST.SUM_OBTAINED AS FLOAT) / NULLIF(ST.SUM_TOTAL, 0) * 100, 2) >= 80 THEN 'A'
            WHEN ROUND(CAST(ST.SUM_OBTAINED AS FLOAT) / NULLIF(ST.SUM_TOTAL, 0) * 100, 2) >= 70 THEN 'B'
            WHEN ROUND(CAST(ST.SUM_OBTAINED AS FLOAT) / NULLIF(ST.SUM_TOTAL, 0) * 100, 2) >= 60 THEN 'C'
            WHEN ROUND(CAST(ST.SUM_OBTAINED AS FLOAT) / NULLIF(ST.SUM_TOTAL, 0) * 100, 2) >= 50 THEN 'D'
            ELSE 'F'
        END AS GRADE
    FROM SubjectPivot S
    INNER JOIN (
        SELECT 
            SCHOOL,
            STUDENT,
            CLASS,
            SECTION,
            [YEAR],
            SMSNO,
            ROLLNO,
            SUM(OBTAINED) AS SUM_OBTAINED,
            SUM(TOTAL) AS SUM_TOTAL
        FROM FilteredSubjects
        GROUP BY SCHOOL, STUDENT, CLASS, SECTION, [YEAR], SMSNO, ROLLNO
    ) ST ON 
        ST.SCHOOL = S.SCHOOL AND 
        ST.STUDENT = S.STUDENT AND 
        ST.CLASS = S.CLASS AND 
        ST.SECTION = S.SECTION AND 
        ST.YEAR = S.YEAR AND 
        ST.SMSNO = S.SMSNO AND 
        ST.ROLLNO = S.ROLLNO
),
Ranked AS (
    SELECT *,
    RANK() OVER (
            PARTITION BY SCHOOL, CLASS, SECTION, [YEAR]
            ORDER BY [%] DESC
        ) AS POSITION
    FROM TotalScores
)
SELECT * FROM Ranked;

GO

-- View: [dbo].[vw_ClassSectionPositions] (Object ID: 965578478)
-- Created: 2025-03-24T23:48:06.470 | Modified: 2025-03-24T23:48:06.470
CREATE VIEW [dbo].[vw_ClassSectionPositions] AS
SELECT 
    -- Select all columns except [%] first
    SCHOOL,
    CLASS,
    SECTION,
    YEAR,
    SUBJECT,
    -- Round % to 2 decimal places
    ROUND([%], 2) AS [%],
    
    -- Add other columns if needed...

    -- Position within Class + Section (for SUBJECT='TOTAL' only)
    DENSE_RANK() OVER (
        PARTITION BY SCHOOL, CLASS, SECTION, YEAR
        ORDER BY [%] DESC
    ) AS POSITION_IN_SECTION,

    -- Position within Class (ignoring Section, for SUBJECT='TOTAL' only)
    DENSE_RANK() OVER (
        PARTITION BY SCHOOL, CLASS, YEAR
        ORDER BY [%] DESC
    ) AS POSITION_IN_CLASS

FROM 
    STUDENTS_RESULT_TOTAL
WHERE 
    [%] IS NOT NULL
    AND SUBJECT = 'TOTAL'
    AND CLASS IN ('6', '7', '8')
    AND YEAR = 25;

GO

-- View: [dbo].[vw_Duplicate_ROLLNO] (Object ID: 955150448)
-- Created: 2025-06-27T17:54:40.570 | Modified: 2025-06-27T17:54:40.570
CREATE VIEW [dbo].[vw_Duplicate_ROLLNO] AS
SELECT
    SCHOOL,
    CLASS,
    YEAR,
    ROLLNO,
    COUNT(*) AS DuplicateCount
FROM STUDENTS_ROLL
GROUP BY
    SCHOOL,
    CLASS,
    YEAR,
    ROLLNO
HAVING COUNT(*) > 1;

GO

-- View: [dbo].[vw_Duplicate_SMSNO] (Object ID: 923150334)
-- Created: 2025-06-27T17:18:42.457 | Modified: 2025-06-27T17:18:42.457
CREATE VIEW [dbo].[vw_Duplicate_SMSNO]
AS
SELECT
    SCHOOL,
    CLASS,
    YEAR,
    SMSNO,
    COUNT(*) AS Occurrences
FROM STUDENTS_ROLL
GROUP BY
    SCHOOL,
    CLASS,
    YEAR,
    SMSNO
HAVING COUNT(*) > 1;

GO

-- View: [dbo].[vw_Expired_Exam_Deadlines] (Object ID: 2070298435)
-- Created: 2026-02-27T22:17:28.780 | Modified: 2026-02-27T22:17:28.780
CREATE VIEW [dbo].[vw_Expired_Exam_Deadlines] AS

SELECT 

    D.[SCHOOL],

    D.[TEACHER],

    D.[CLASS],

    D.[SECTION],

    D.[GROUP],

    D.[SUBJECT],

    D.[EXAMTYPE],

    D.[YEAR],

    D.[TOTALCOUNT],

    D.[ENTRIES_MARKED],

    D.[INPUTCOMPLETED %],

    D.[RESULTCOMPLETED %],

    E.[STARTDATE] AS [Start Date],

    E.[ENDDATE] AS [End Date],

    DATEADD(day, 5, E.[ENDDATE]) AS [ExpiryDate],

    -- Helper column for days overdue

    DATEDIFF(day, DATEADD(day, 5, E.[ENDDATE]), GETDATE()) AS [DaysPastDeadline]

FROM [db_aadc11_sqldaanish].[dbo].[Data_Entry_Status_View] D

-- 1. Join with Schedule to check dates

INNER JOIN [db_aadc11_sqldaanish].[dbo].[Exam_Schedule_26] E 

    ON D.[SCHOOL] = E.[SCHOOL] 

    AND D.[CLASS] = E.[CLASS] 

    AND D.[SECTION] = E.[SECTION]

    AND D.[EXAMTYPE] = E.[EXAM]

    AND D.[YEAR] = E.[YEAR]

-- 2. Join with Mapping table to validate Subject-Group combination

INNER JOIN [db_aadc11_sqldaanish].[dbo].[SUBJECT_GORUP_YEAR_MARKS_26] M

    ON D.[SUBJECT] = M.[SUBJECT]

    AND D.[GROUP] = M.[GROUP]

    AND D.[CLASS] = M.[CLASS]

    AND D.[YEAR] = M.[YEAR]

    AND D.[EXAMTYPE] = M.[EXAM]

WHERE D.[INPUTCOMPLETED %] < 100 

  AND GETDATE() > DATEADD(day, 5, E.[ENDDATE]);

GO

-- View: [dbo].[vw_Marks_Preview_Class8] (Object ID: 850818093)
-- Created: 2026-04-09T08:47:09.190 | Modified: 2026-04-09T08:47:09.190
CREATE VIEW [dbo].[vw_Marks_Preview_Class8]
AS
SELECT 
    Sub.SubjectName AS [SUBJECT],
    NULL AS [OBTAINED], 
    100 AS [TOTAL], 
    NULL AS [%], 
    NULL AS [GRADE], 
    NULL AS [STATUS], 
    REPLACE(S.[BOARDROLLNO], '-', '') AS [CLEANED_BOARD_ROLLNO],
    S.[ROLLNO] AS [INTERNAL_ROLLNO],
    S.[CLASS], 
    S.[YEAR], 
    S.[EXAM] AS [EXAMTYPE],
    NULL AS [Remarks],
    S.[SCHOOL],
    S.[STUDENT],
    S.[FATHER]
FROM [db_aadc11_sqldaanish].[dbo].[STUDENTS_ROLL_INTERNAL_EXAM] AS S
CROSS JOIN (
    SELECT 'ENGLISH' AS SubjectName UNION ALL
    SELECT 'URDU' UNION ALL
    SELECT 'MATHEMATICS' UNION ALL
    SELECT 'GENERAL SCIENCE'
) AS Sub
WHERE S.[CLASS] = '8' 
  AND S.[EXAM] = 'ANNUAL' 
  AND S.[YEAR] = '26'
  AND S.[SCHOOL] NOT IN ('MNKB', 'MNKG', 'TNSG', 'TNSB')
  AND S.[BOARDROLLNO] IS NOT NULL 
  AND TRIM(S.[BOARDROLLNO]) <> '';

GO

-- View: [dbo].[vw_MissingResultsWithStatus] (Object ID: 299148111)
-- Created: 2025-06-16T23:25:27.797 | Modified: 2025-06-16T23:25:27.797
CREATE VIEW [dbo].[vw_MissingResultsWithStatus] AS
WITH expected_subjects AS (
    SELECT
        r.SMSNO, r.ROLLNO, r.STUDENT, r.FATHER, r.SCHOOL, r.YEAR,
        r.CLASS, r.SECTION, r.CATEGROY, r.[GROUP], m.SUBJECT AS ExpectedSubject
    FROM STUDENTS_ROLL r
    JOIN SUBJECT_GROUP_YEAR_MARKS m
      ON r.YEAR = m.YEAR AND r.CLASS = m.CLASS AND r.[GROUP] = m.[GROUP]
),
actual_subjects AS (
    SELECT
        SCHOOL, ROLLNO, YEAR, SECTION, CLASS, [GROUP], STUDENT, FATHER, SUBJECT
    FROM STUDENTS_RESULT_TOTAL
),
missing_subjects AS (
    SELECT e.*
    FROM expected_subjects e
    LEFT JOIN actual_subjects a
      ON e.SCHOOL = a.SCHOOL AND e.ROLLNO = a.ROLLNO AND e.YEAR = a.YEAR
         AND e.SECTION = a.SECTION AND e.CLASS = a.CLASS
         AND e.[GROUP] = a.[GROUP] AND e.STUDENT = a.STUDENT
         AND e.FATHER = a.FATHER AND a.SUBJECT = e.ExpectedSubject
    WHERE a.SUBJECT IS NULL
)
SELECT
    m.SMSNO,
    m.ROLLNO,
    m.STUDENT,
    m.FATHER,
    m.SCHOOL,
    m.YEAR,
    m.CLASS,
    m.SECTION,
    m.CATEGROY,
    m.ExpectedSubject,
    CASE 
        WHEN EXISTS (
            SELECT 1
            FROM dbo.ABSENT a
            WHERE a.ROLLNO = m.ROLLNO
              AND LTRIM(RTRIM(a.SUBJECT)) = LTRIM(RTRIM(m.ExpectedSubject))
              AND a.CLASS = m.CLASS
              AND CAST(a.YEAR AS VARCHAR) = CAST(m.YEAR AS VARCHAR)
              AND a.SCHOOL = m.SCHOOL
        ) THEN 'Absent'
        ELSE 'Missing'
    END AS Status
FROM missing_subjects m;

GO

-- View: [dbo].[vw_Missing_Results_Base] (Object ID: 283148054)
-- Created: 2025-06-16T23:14:16.630 | Modified: 2025-06-16T23:15:15.460
CREATE VIEW [dbo].[vw_Missing_Results_Base] AS
WITH expected_subjects AS (
    SELECT
        r.SCHOOL, r.ROLLNO, r.YEAR, r.SECTION, r.CLASS, r.[GROUP],
        r.STUDENT, r.FATHER, m.SUBJECT
    FROM STUDENTS_ROLL r
    JOIN SUBJECT_GROUP_YEAR_MARKS m
      ON r.YEAR = m.YEAR AND r.CLASS = m.CLASS AND r.[GROUP] = m.[GROUP]
),
actual_subjects AS (
    SELECT
        SCHOOL, ROLLNO, YEAR, SECTION, CLASS, [GROUP], STUDENT, FATHER, SUBJECT
    FROM STUDENTS_RESULT_TOTAL
),
missing_subjects AS (
    SELECT e.*
    FROM expected_subjects e
    LEFT JOIN actual_subjects a
      ON e.SCHOOL = a.SCHOOL AND e.ROLLNO = a.ROLLNO AND e.YEAR = a.YEAR
         AND e.SECTION = a.SECTION AND e.CLASS = a.CLASS
         AND e.[GROUP] = a.[GROUP] AND e.STUDENT = a.STUDENT
         AND e.FATHER = a.FATHER AND e.SUBJECT = a.SUBJECT
    WHERE a.SUBJECT IS NULL
)
SELECT * FROM missing_subjects;

GO

-- View: [dbo].[vw_SCHOOL_SUBJECT_WISE_POS] (Object ID: 644197345)
-- Created: 2025-08-30T12:17:41.490 | Modified: 2025-08-30T12:17:41.490
CREATE VIEW [dbo].[vw_SCHOOL_SUBJECT_WISE_POS] AS
SELECT 
    SCHOOL,
    CLASS,
    YEAR,
    SUBJECT,
    SUM(OBTAINED) AS OBTAINED,
    SUM(TOTAL) AS TOTAL,
    CAST(SUM(OBTAINED) * 100.0 / NULLIF(SUM(TOTAL),0) AS DECIMAL(5,2)) AS [%]
FROM students_result_total
GROUP BY 
    SCHOOL,
    CLASS,
    YEAR,
    SUBJECT;

GO

-- View: [dbo].[vw_School_Mock_Performance_Summary] (Object ID: 2086298492)
-- Created: 2026-02-28T00:16:28.100 | Modified: 2026-02-28T00:16:28.100
CREATE VIEW [dbo].[vw_School_Mock_Performance_Summary] AS
WITH LatestMocks AS (
    -- Step 1: Find latest Mock where the 5-day grace period has passed
    SELECT 
        SCHOOL, 
        CLASS, 
        MAX(EXAM) AS LatestMockExam,
        MAX(DATEADD(day, 5, ENDDATE)) AS DeadlineDate -- 5 Days past End Date
    FROM [db_aadc11_sqldaanish].[dbo].[Exam_Schedule_26]
    WHERE EXAM LIKE 'MOCK%' 
      AND DATEADD(day, 5, ENDDATE) <= GETDATE()
    GROUP BY SCHOOL, CLASS
),
StudentOverallResults AS (
    -- Step 2: Calculate OVERALL % per student to avoid double-counting subjects
    SELECT 
        V.SCHOOL,
        V.CLASS,
        V.ROLLNO,
        V.EXAM,
        (SUM(CAST(V.OBTAINED AS FLOAT)) / NULLIF(SUM(CAST(V.TOTAL AS FLOAT)), 0)) * 100 AS Overall_Percentage
    FROM [db_aadc11_sqldaanish].[dbo].[INTERNAL_STUDENT_RESULT_CARD_VIEW] V
    INNER JOIN LatestMocks LM ON V.SCHOOL = LM.SCHOOL 
        AND V.CLASS = LM.CLASS 
        AND V.EXAM = LM.LatestMockExam
    WHERE V.YEAR = '26'
    GROUP BY V.SCHOOL, V.CLASS, V.ROLLNO, V.EXAM
),
CurrentMockFinalCounts AS (
    -- Step 3: Student counts per bracket based on their overall percentage
    SELECT 
        SCHOOL,
        CLASS,
        EXAM,
        COUNT(DISTINCT ROLLNO) AS APPEARED_STUDENTS,
        SUM(CASE WHEN Overall_Percentage >= 90 THEN 1 ELSE 0 END) AS [90-100_Cnt],
        SUM(CASE WHEN Overall_Percentage >= 80 AND Overall_Percentage < 90 THEN 1 ELSE 0 END) AS [80-89_Cnt],
        SUM(CASE WHEN Overall_Percentage >= 70 AND Overall_Percentage < 80 THEN 1 ELSE 0 END) AS [70-79_Cnt],
        SUM(CASE WHEN Overall_Percentage >= 50 AND Overall_Percentage < 60 THEN 1 ELSE 0 END) AS [50-59_Cnt],
        SUM(CASE WHEN Overall_Percentage >= 40 AND Overall_Percentage < 50 THEN 1 ELSE 0 END) AS [40-49_Cnt],
        SUM(CASE WHEN Overall_Percentage < 40 THEN 1 ELSE 0 END) AS [Below_40_Cnt]
    FROM StudentOverallResults
    GROUP BY SCHOOL, CLASS, EXAM
),
MissedEntriesStats AS (
    -- Step 4: Missed Entries excluding non-core Class 8 subjects
    SELECT 
        SCHOOL,
        CLASS,
        EXAMTYPE,
        SUM(TOTALCOUNT - ENTRIES_MARKED) AS TOTAL_MISSED_ENTRIES
    FROM [db_aadc11_sqldaanish].[dbo].[vw_Expired_Exam_Deadlines]
    WHERE YEAR = '26'
      AND NOT (CLASS = '8' AND SUBJECT NOT IN ('ENGLISH', 'URDU', 'MATHEMATICS', 'GENERAL SCIENCE'))
    GROUP BY SCHOOL, CLASS, EXAMTYPE
),
HistoricalStats AS (
    -- Step 5: Historical 80-100% (Corrected to never exceed 100%)
    SELECT 
        SCHOOL,
        CLASS,
        CAST(SUM(CASE WHEN Year = '25' THEN (Count_90_100 + Count_80_90) ELSE 0 END) * 100.0 / 
             NULLIF(SUM(CASE WHEN Year = '25' THEN APPEARED ELSE 0 END), 0) AS DECIMAL(5,2)) AS [80-100_Pct_YR25],
        CAST(SUM(CASE WHEN Year = '24' THEN (Count_90_100 + Count_80_90) ELSE 0 END) * 100.0 / 
             NULLIF(SUM(CASE WHEN Year = '24' THEN APPEARED ELSE 0 END), 0) AS DECIMAL(5,2)) AS [80-100_Pct_YR24]
    FROM [db_aadc11_sqldaanish].[dbo].[TR_ALL]
    GROUP BY SCHOOL, CLASS
)
-- Final View Assembly
SELECT 
    C.SCHOOL,
    C.CLASS,
    C.EXAM AS [LATEST_MOCK_COMPLETED],
    C.APPEARED_STUDENTS,
    C.[90-100_Cnt] AS [90-100_COUNT],
    C.[80-89_Cnt] AS [80-89_COUNT],
    C.[70-79_Cnt] AS [70-79_COUNT],
    C.[50-59_Cnt] AS [50-59_COUNT],
    C.[40-49_Cnt] AS [40-49_COUNT],
    C.[Below_40_Cnt] AS [BELOW_40_COUNT],
    (C.[90-100_Cnt] + C.[80-89_Cnt] + C.[70-79_Cnt]) AS [70-100_TOTAL_COUNT],
    ISNULL(M.TOTAL_MISSED_ENTRIES, 0) AS [MISSED_ENTRIES],
    ISNULL(H.[80-100_Pct_YR25], 0) AS [80-100%_YR25],
    ISNULL(H.[80-100_Pct_YR24], 0) AS [80-100%_YR24],
    LM.DeadlineDate AS [MOCK_DEADLINE] -- Final Column
FROM CurrentMockFinalCounts C
INNER JOIN LatestMocks LM ON C.SCHOOL = LM.SCHOOL AND C.CLASS = LM.CLASS
LEFT JOIN MissedEntriesStats M ON C.SCHOOL = M.SCHOOL 
    AND C.CLASS = M.CLASS 
    AND C.EXAM = M.EXAMTYPE
LEFT JOIN HistoricalStats H ON C.SCHOOL = H.SCHOOL AND C.CLASS = H.CLASS;

GO

-- View: [dbo].[vw_StudentCategoryStrength] (Object ID: 89767377)
-- Created: 2025-11-22T19:44:42.670 | Modified: 2026-01-27T04:31:01.177
CREATE VIEW [dbo].[vw_StudentCategoryStrength]
AS
SELECT
    -- Synthetic ID placeholder
    CAST(NULL AS VARCHAR(10)) AS ID, 
    
    T.SCHOOL,
    
    -- Added EXAM column here
    T.EXAM,
    
    -- Use COALESCE to label the Class summaries
    COALESCE(CAST(T.CLASS AS VARCHAR(10)), 'ALL CLASSES') AS CLASS,
    
    -- Use CASE WHEN and GROUPING() to label the Section summaries
    CASE
        -- Summary of all sections within a specific CLASS for a specific EXAM
        WHEN GROUPING(SECTION) = 1 AND GROUPING(CLASS) = 0 THEN 'ALL'
        -- Whole School summary for a specific EXAM
        WHEN GROUPING(CLASS) = 1 THEN 'Whole School'
        ELSE T.SECTION
    END AS SECTION,
    
    T.YEAR,
    
    -- Count of students for the specific grouping level and EXAM
    COUNT(*) AS CountOfStudents  
    
FROM
    dbo.STUDENTS_ROLL_INTERNAL_EXAM AS T
GROUP BY
    GROUPING SETS
    (
        -- 1. Section Total per Exam: SCHOOL + EXAM + CLASS + SECTION + YEAR
        (T.SCHOOL, T.EXAM, T.CLASS, T.SECTION, T.YEAR), 
        
        -- 2. Class Total ('ALL' Section) per Exam: SCHOOL + EXAM + CLASS + YEAR
        (T.SCHOOL, T.EXAM, T.CLASS, T.YEAR),
        
        -- 3. Whole School Total per Exam: SCHOOL + EXAM + YEAR
        (T.SCHOOL, T.EXAM, T.YEAR)
    )

GO

-- View: [dbo].[vw_TR_ALL_CF] (Object ID: 692197516)
-- Created: 2025-09-03T11:39:17.103 | Modified: 2025-09-03T11:39:17.103
CREATE VIEW [dbo].[vw_TR_ALL_CF] AS
SELECT
    ROW_NUMBER() OVER (ORDER BY T.SUBJECT, T.CLASS, T.YEAR, T.SCHOOL) AS [Serial No],
    T.EID,
    T.NAME,
    T.SCHOOL,
    T.EXAMTYPE AS [EXAM TYPE],
    T.SUBJECT,
    T.CLASS,
    T.SECTION,
    T.YEAR,
    T.CATEGROY,
    T.STRENGTH,
    T.Count_90_100 AS [Above 90%],
    T.Count_80_90  AS [Above 80%],
    T.Count_70_80  AS [Above 70%],
    T.Count_60_70  AS [Above 60%],
    T.Count_50_60  AS [Above 50%],
    T.Count_40_50  AS [Above 40%],
    T.Count_0_39   AS [Below 40%],
    T.APPEARED     AS [Appeared Students],
    T.PASSED,
    T.[PASS%]      AS [PASS %age],
    T.[CLASS AVG],
    A.[%]          AS [School (Subject) Avg marks %age],
    CAST(ROUND(T.[CLASS AVG] - A.[%] + 3, 2) AS DECIMAL(5, 2)) AS CF
FROM
    TR_ALL T
LEFT JOIN
    vw_CLASS_YEAR_SUBJECT_AGGREGATE A
    ON  T.CLASS = A.CLASS
    AND T.YEAR = A.YEAR
    AND T.SUBJECT = A.SUBJECT;

GO

-- View: [dbo].[vw_Teacher_IncorrectSubjects] (Object ID: 507148852)
-- Created: 2025-06-18T10:53:46.973 | Modified: 2025-06-18T10:53:46.973
CREATE VIEW [dbo].[vw_Teacher_IncorrectSubjects] AS
SELECT 
    T.SCHOOL, 
    T.YEAR, 
    T.CLASS, 
    T.SECTION, 
    T.SUBJECT AS Incorrect_Subject
FROM 
    TEAHCERS T
LEFT JOIN 
    CorrectSubjects CS 
    ON LTRIM(RTRIM(T.SUBJECT)) = LTRIM(RTRIM(CS.SUBJECT))
    AND T.CLASS = CS.CLASS
WHERE 
    CS.SUBJECT IS NULL
GROUP BY 
    T.SCHOOL, 
    T.YEAR, 
    T.CLASS, 
    T.SECTION, 
    T.SUBJECT;

GO
