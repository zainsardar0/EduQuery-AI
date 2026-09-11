SET NOCOUNT ON;
SET XACT_ABORT ON;

BEGIN TRANSACTION;
UPDATE eduquery_reporting.SemanticContract
SET IsActive = 0
WHERE ContractVersion = '2026.08.16.1' AND IsActive = 1;
COMMIT TRANSACTION;

-- This rollback deliberately preserves reporting objects and evidence.
-- The API readiness check fails closed until an accepted contract is activated.
