import argparse
todolist = {
        "tungtung": False,
        "sigmaboy": True
    }
selectedone = "idk"



def renderthing(selectedchoice):
    # i imagine it like
    # [ ] tungtung
    # [X] sigmaboy

    
    for i in todolist:
        
        cross = ""
        if todolist[i] == False:
            cross = "[X]"
        else:
            cross = "[ ]"
        
        print(cross, i)

        



def cli():
    # parser = argparse.ArgumentParser(description="Test")

    # parser.add_argument("test", help="Testing")

    # args = parser.parse_args()

    # print(args.test)
    ## ^ for later
    renderthing()
    



if __name__ == "__main__":
    cli()