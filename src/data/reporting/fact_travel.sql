CREATE VIEW [dbo].[v_fact_travel]
AS
select 
	TravelId, 
	TravelType,
	TravelNo as RefNo,
	StartDate,
	EndDate,
	TravelDays,
	Origin,
	Destination,
	Transportation,
	[WorkEmail] as UserEmail,
	CASE(c.InfoName) WHEN 'deleted' THEN 'Cancelled' ELSE c.infoname END as [Status],
	[StatusUser],
	[StatusDate] as [StatusUpdateDate],
	a.CrtDate as [CreatedDate]
from dbo.SYS_TRAVEL_DETAIL a
INNER JOIN
dbo.SYS_FRAME_BaseInfo AS c ON c.InfoCode = a.Status AND c.InfoTypeID = 'TravelTaskStatus'