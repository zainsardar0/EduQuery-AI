SET NOCOUNT ON;
SET XACT_ABORT ON;

IF CONVERT(nvarchar(60), DATABASEPROPERTYEX(DB_NAME(), 'Updateability')) <> N'READ_WRITE'
    THROW 51000, 'EduQuery migrations require a writable deployment target.', 1;

IF SCHEMA_ID(N'eduquery_reporting') IS NULL
    EXEC(N'CREATE SCHEMA eduquery_reporting AUTHORIZATION dbo;');

IF OBJECT_ID(N'eduquery_reporting.SemanticContract', N'U') IS NULL
BEGIN
    CREATE TABLE eduquery_reporting.SemanticContract (
        ContractVersion varchar(32) NOT NULL,
        IsActive bit NOT NULL CONSTRAINT DF_SemanticContract_IsActive DEFAULT (0),
        AppliedAt datetime2(0) NOT NULL CONSTRAINT DF_SemanticContract_AppliedAt DEFAULT (SYSUTCDATETIME()),
        ActivatedAt datetime2(0) NULL,
        AppliedBy sysname NOT NULL CONSTRAINT DF_SemanticContract_AppliedBy DEFAULT (ORIGINAL_LOGIN()),
        SourceRevision varchar(64) NULL,
        CONSTRAINT PK_SemanticContract PRIMARY KEY (ContractVersion)
    );
END;

IF OBJECT_ID(N'eduquery_reporting.PassThresholdRule', N'U') IS NULL
BEGIN
    CREATE TABLE eduquery_reporting.PassThresholdRule (
        RuleId int IDENTITY(1,1) NOT NULL,
        ClassFrom tinyint NOT NULL,
        ClassTo tinyint NOT NULL,
        YearFrom smallint NOT NULL,
        YearTo smallint NOT NULL,
        PassPercentageExclusive decimal(5,2) NOT NULL,
        IsActive bit NOT NULL CONSTRAINT DF_PassThresholdRule_IsActive DEFAULT (1),
        ApprovedBy nvarchar(200) NOT NULL,
        SourceReference nvarchar(500) NOT NULL,
        ApprovedAt datetime2(0) NOT NULL,
        CONSTRAINT PK_PassThresholdRule PRIMARY KEY (RuleId),
        CONSTRAINT CK_PassThresholdRule_Class CHECK (ClassFrom BETWEEN 1 AND 12 AND ClassTo BETWEEN ClassFrom AND 12),
        CONSTRAINT CK_PassThresholdRule_Year CHECK (YearTo >= YearFrom),
        CONSTRAINT CK_PassThresholdRule_Percentage CHECK (PassPercentageExclusive BETWEEN 0 AND 100)
    );
END;

IF OBJECT_ID(N'eduquery_reporting.MaterializationState', N'U') IS NULL
BEGIN
    CREATE TABLE eduquery_reporting.MaterializationState (
        ObjectName sysname NOT NULL,
        LastStartedAt datetime2(0) NULL,
        LastSucceededAt datetime2(0) NULL,
        [RowCount] bigint NULL,
        DurationMs int NULL,
        LastErrorCode varchar(64) NULL,
        CONSTRAINT PK_MaterializationState PRIMARY KEY (ObjectName)
    );
END;

IF NOT EXISTS (
    SELECT 1 FROM eduquery_reporting.SemanticContract WHERE ContractVersion = '2026.08.16.1'
)
BEGIN
    INSERT eduquery_reporting.SemanticContract (ContractVersion, IsActive)
    VALUES ('2026.08.16.1', 0);
END;
