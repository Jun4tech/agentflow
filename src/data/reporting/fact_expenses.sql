CREATE VIEW [dbo].[v_fact_expenses]
as
with exp_type as (
	select InfoCode, InfoName as ExpenseType from [dbo].[SYS_FRAME_BaseInfo] where infotypeid='ExpenseType' and isvalid=1
),
exp_status as (
	select InfoCode, InfoName as [Status] from [dbo].[SYS_FRAME_BaseInfo] where infotypeid='expensestatus' and isvalid=1
)
select [Owner] as UserEmail, exp_type.ExpenseType, DetailTypeName as ExpenseDetail, Currency, Expensed as ExpenseAmount, CrtDate as CreateDate,
exp_main.refno as RefNo  
from [dbo].[SYS_EXPENSE_MASTER] exp_main
inner join [dbo].[SYS_EXPENSE_DETAIL] exp_det on exp_main.ExpenseID = exp_det.ExpenseID
left join exp_type on exp_type.InfoCode = exp_main.ExpenseType
left join exp_status on exp_status.InfoCode = exp_main.[Status]
