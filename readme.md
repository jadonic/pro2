# PROG-2 Project Nicolas Steiger

As my PROG-2 project I simulate a wrestling tournament. To keep it as simple as possible the wrestling tournament consists of only one weight class. As usual at international tournaments a weight class consists of eight participants.

## Create participant

The first step is to create a new participant. This can be done by using the displayed input fields. It is important that all fields are filled in. With the button "Enter" the participant is entered. If you want, you can also generate a random wrestler. This will be randomly composed from a selection of 20 first names, 20 last names, 20 countries and 10 weights.

When the entry is made, a random lot between 1 and 99 is automatically assigned. This process simulates the drawing of lots during the weigh-in at a real tournament. The lot is used (as in a real tournament) as the basis for the initial division of fights. 

To start the fight simulation **eight participants must be entered**. Before the fight simulation, the list of participants can be deleted and recreated if necessary.
## Weight limits
In wrestling, each weight class has a lower and an upper limit. So you can't be too light or too heavy for it. For the 74kg weight class, the lower weight limit is 65kg and the upper weight limit is 74kg. These limits have been set accordingly in the relevant html element.

## Combat simulation
The tournament works in a pool system. The winners of the 1st round end up in the winner pool and the losers of the 1st round end up in the loser pool. A winner of the 2nd round has to fight against the other winner of the corresponding pool. The same for the losers of the 2nd round. After the fights in the 3rd round the order and therefore the ranking is already fixed.

![Screenshot tournament logic](/assets/images/ScreenshotTurnierlogik.jpg)

### Rules 
In a wrestling match, the winner is the participant who has more points at the end of the time, or who manages to build up a 15-point difference over his opponent during the match (e.g. 15:0 or 18:3). In practice, a single score rarely if ever exceeds 30 points, so this score limit was set in the program.

So in the simulation we can record the respective points of the wrestlers and thus the winner of a match. It is irrelevant whether the fight was finished during the fighting time or at the end of it. 

#### Tie
Although rather rare, it can happen that a fight ends with the same number of points. In practice, several rules come into play in this case:
* Number of penalty points
* amount of the individual scores
* who made the last point

**There is therefore ALWAYS a winner.** In the fight simulation, in the event of a tie, a random winner is therefore selected.

## Ranking list and restart
The ranking list is relatively self-explanatory. The wrestlers are sorted in ascending order based on their score and ranked in the list. 

If necessary, you have the possibility to reset all databases and then restart the wrestling tournament.

## Json wrestler database and tournament database
### Wrestler database
The wrestling database is designed to store basic information about a wrestler, as well as the data on tournaments he has been to. 

#### Basic information

* wrestlerID
* first name
* surname
* country

#### tournament data

* weight
* weight class
* lot number

This database was deliberately kept simple, with the background that it can be expanded at any time, if further work on the project would be.

### Tournament database
The tournament database is a temporary database that represents the current tournament. On the one hand, this database contains basic information about the tournament

* Tournament name
* weight classes
* fight history

and on the other hand values, which must be stored for the fight logic:

* wrestlerindex
* round counter
* fight counter
* round points
* fightid

This database was designed with the prospect that, if the function is expanded, instead of just one tournament, several tournaments can be stored in a kind of "tournament history".