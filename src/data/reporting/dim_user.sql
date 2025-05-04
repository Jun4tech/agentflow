CREATE VIEW [dbo].[v_dim_user]
as
select recid as UserId, FullName, WorkEmail as UserEmail, JobTitle, Department, IsActive from [dbo].[SYS_PROFILE_BASE]
