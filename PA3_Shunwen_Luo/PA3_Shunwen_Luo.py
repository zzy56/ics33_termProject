from cardTable import cardTable
import argparse
import dealer
import file_mode
if __name__ == '__main__':
    # def functionName(level):
    #     #Raise an non-number input error
    #     if level < 0:
    #         raise Exception('Please input a number more than 0.')
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', action="store_true",
                        help='Stop the game')
    parser.add_argument('-f', action="store_true",
                        help='Stop the game')
    parser.add_argument('-p', type=int, default=0,
                        help='Bot players ')
    parser.add_argument('-i', type=str, default=0,
                        help='Bot players ')

    args = parser.parse_args()

    def functionName(level):
        # Raise an non-number input error
        if level <= 0:
            raise Exception("Invalid Input")
    #print(args.f)
    if args.u:
        n_player = args.p
        try:
            #print(n_player)
            functionName(n_player)
            cardTable().set_up_table(n_player)
        except:
            print('error.')

    elif args.f:
        file_fold = args.i
        a=file_mode.main(file_fold)
        print('Pass test number:',a)




    '''try:
        print(n_player)
        functionName(n_player)
        cardTable(dealer()).set_up_table(n_player)
    except:
        print('error.')'''
'''def functionGameMode(mode):
        #Raise an non-number input error
        if not mode == 1 and not mode == 2:
            raise Exception('Game mode error.')
    x=True
    while x:
        try:
            # num_p = int(input("Number of players:"))  #number of player
            # functionName(num_p)
            # game_time = int(input("Number of games:")) #number of games
            # functionName(game_time)
            gamemode = int(input("""
Game Mode:
1.God's perspective
2.Player mode
Please select:
"""))
            functionGameMode(gamemode)

            cardTable(gameMode(gamemode)).set_up_table(5)
            x=False
        except:
            print('error.')'''
 