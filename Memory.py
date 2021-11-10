# implementation of card game - Memory

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# helper function to initialize globals
def new_game():
    global memory_deck #Create deck of 16 cards - 8 pairs
    memory_deck = range(0,8) + range(0,8)
    random.shuffle(memory_deck) #Shuffle
    global exposed
    exposed = [False]*16 #All face down
    global state #Initial state
    state = 0
    global turn_counter #Counting n(turns)
    turn_counter = 0
    label.set_text("Turns = " + str(turn_counter))
    
    
# define event handlers
def mouseclick(pos):
    global state
    global opened_card
    global opened_card2
    global turn_counter
    if state == 0: #All cards face down prior to first click
        if not exposed[pos[0]//50]:
            exposed[pos[0]//50] = True
            opened_card = pos[0]//50 #Store index of first opened card
            state = 1 
    elif state == 1: #At this point one card is face up
        if not exposed[pos[0]//50]:
            exposed[pos[0]//50] = True
            opened_card2 = pos[0]//50 #Store index of second opened card
            turn_counter += 1 #Increment turn counter and update label
            label.set_text("Turns = " + str(turn_counter))
            state = 2
    else: #Now two cards are face up
        #Before clicking we check immediately whether the opened cards match        
        #If not, cover them both before even clicking
        #Either way, we begin our search for a new pair
        #This is the first card of a new prospective pair
        if not exposed[pos[0]//50]:            
            if memory_deck[opened_card] != memory_deck[opened_card2]:
                exposed[opened_card] = False 
                exposed[opened_card2] = False            
            exposed[pos[0]//50] = True
            opened_card = pos[0]//50 #So store this index
            state = 1
                               
# cards are logically 50x100 pixels in size    
def draw(canvas):
    numbercounter = 15
    cardcounter = 0
    card_index = 0
    for i in exposed: #Use exposed T/F to determine if number or card is drawn
        if i:
            canvas.draw_text(str(memory_deck[card_index]),
                             [numbercounter, 60], 40, "White")
        else:
            canvas.draw_polygon([[cardcounter,0],[cardcounter, 100],
                                 [cardcounter+50,100],[cardcounter+50,0]],
                                3, "Brown", "Green")
        numbercounter += 50
        cardcounter += 50
        card_index += 1

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
