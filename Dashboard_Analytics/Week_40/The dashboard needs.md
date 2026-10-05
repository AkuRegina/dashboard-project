## **1.	Purpose**
The purpose of the dashboard is to provide managers, supervisors, and assigned personnel with a clear overview of deviations during the construction process. 
The dashboard must enable users to view, manage, and track deviations, while also providing analysis of the current situation and assisting in trend identification.

## **2.	Target Users**
The dashboard is expected to support two main user perspectives:
-	Manager / Supervisor:
•	Monitor all deviations.
•	Assign deviations to users.
•	Monitor deviation status and deadlines.
•	Review deviation details and attached images.
•	Use analytics to understand the overall situation.
-	Assigned Worker:
•	View deviations assigned to them.
•	View deviation details and related images.
•	Follow the status and deadline of assigned deviations.
•	Participate in discussions/comments.

## **3.	Dashboard Information**
-	The dashboard should provide a quick overview of:
•	Total number of deviations
•	Open deviations
•	Deviations in progress
•	Closed deviations
•	Overdue deviations
•	Deviations assigned to me

## **4.	Deviation Information**
-	When a user opens a deviation, the dashboard should display:
•	Drawing
•	Assembly / ship
•	Deviation type
•	Severity
•	Description
•	Submitted by
•	Assigned user
•	Status
•	Deadline
•	Attached images
•	Comments / discussion

## **5.	Dashboard Actions**
-	Users should be able to:
•	View deviation details
•	Search deviations
•	Filter deviations
•	View assigned deviations
•	Change deviation status
•	Assign a deviation to a user
•	View attached images
•	View and add comments

## **6.	Satus Workflow**
-	The project specifies three deviation statuses:
Open → In Progress → Closed
|   Status    |	            Meaning                                    |
|-------------|--------------------------------------------------------|
| Open	      |The deviation has been reported and requires attention. |
| In Progress |	Someone is currently working on the deviation.         |
| Closed      |	The deviation has been resolved.                       |

## **7.	Deadlines**
-	Each deviation should have a deadline for resolution:
•	Upcoming deadlines
•	Deviations due soon
•	Overdue deviations

## **8.	Analytics**
-	Analytics should have:
•	Deviations by type
•	Open vs. Closed deviations
•	Deviations by severity
•	Deviations over time
•	Overdue deviations
•	Deviations by assigned user

## **9.	Dashboard Structure**

|                   Dashboard                   |
|-----------------------------------------------|
| Total | Open | In Progress | Closed | Overdue |
|-------|------|-------------|--------|---------|
| 120   | 35   | 20          | 65     | 8       |

| Deviations by Type |     | Deviations by Status |
|--------------------|     |----------------------|
| Safety             |     |Open                  |
| Design             |     | In Progress          |
| Construction       |     | Closed               |

|            My Assigned Deviations             |
|-----------------------------------------------|
|  ID   |   Type   | Severity  |   Status    |  Deadline  |
|-------|----------|-----------|-------------|------------|
| 101   | Safety   | High      | Open        | 20/10/2026 |
| 102   | Design   | Medium    | In Progress | 23/10/2026 |
