# Texas Hold'em poker game

Texas Hold'em poker is a game module for people who want to play with bot players.
## Features
This program includes several files :
- PA3_Shunwen_Luo.py (main program, which trigger user mode and player mode )
- cardTable.py (execute user mode)
- dealer.py (deal cards)
- file_mode.py (execute file mode)
- player.py (encapsulate player information)
- poker.py (encapsulate poker information)
- pokerHands.py (get rank)
- pokerHandsType.py (make sure rank is int to avoid misuse)
- tie_breaker.py (judge the tie condition)

## Usage
This is a package of play Texas Hols'em poker game and use test case to get right rank.
### User mode 
Open the PA3_Shunwen_Luo.py. Use command to test for User mode.
```
python PA3_Shunwen_Luo.py -u -p {number of players}
```
> Note: `{number of players}` needs to be specified by user and it should be an int.

Then it will ask for fold or bet. Enter 1 will choose fold and enter 2 will choose bet. 
```
1
```
If user chooses 1, all will proceed on their own until the end of a game. 
```
2
```
If user chooses 2, user needs to enter a number of money to bet.
```
{number of money}
```
> Note: `{number of money}` needs to be specified by user and it should be an int.

This question of whether to fold or bet will last three times. After three times, the game will end and the player will be asked to continue or exit. Enter 1 will choose continue and enter 2 will choose exit.

```
1
```
If user chooses 1, the game will restart, but the player's money will remain as it was at the end of the previous game. Players with less than or equal to 0 money will be eliminated.
```
2
```
If user chooses 2, the game ends.

### File mode
Open the PA3_Shunwen_Luo.py. Use command to test for File mode.
```
python PA3_Shunwen_Luo.py -f -i {path_to_test_cases_directory}
```
> Note: `{path_to_test_cases_directory}` needs to be specified by user and it is required.

There is no other action and it will print how many test cases will pass the test.



