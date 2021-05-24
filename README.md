# AI
uses Pacman game as the platform and transforms pacman agent to the intellingnt agent using different AI techniques


<h1> Search implementation: </h1>

Question q1: i used lecture help on doing the depth first search, creates a stack for keeing track of fringe, uses list 
             to keep track of visited spotsoriginally used set() but gave error on later question where mix match of list
             and set happened so i changed the set to list on all problems. so the agent visits the node and push node to 
             the list and if it reaches the goal, the search problem is finished

Question 2: bfs developed in a very similar way except it used queue data structure to keep track of path for all shallow 
            spot on the breadth, when pacman reached goal state, search terminates

Question 3: uniform cost search used priority queue to better find the path where it kept track of cheapest path to the
            possible goal state,the agent would explore the cheapest path first and then come for expensive path if path 
            not found, when reached the goal state, search terminates

Question 4: A* search also used priority queue but also introduced heuristics to find shortest possible path to the goal.
            It is more informed in a sense it uses heuristic to determine whether the path is closest to the goal state

question 5: finding all the corner used a list to track down all the corners, if the corner is not visited, the pacman
            would append the list when gets visited. agent checks for the wall in the successor state, if not wall, it 
            marks the position as visited and also checks if the position was a corner, if corner puts in the list of 
            visited corner. When all corners are visited, the search terminates

Question 6: in this problem, on the first try, i tried to use the distance between the points finding absolute value of 
            sum and difference of two cordinate points as 
            abs(Xcur - Xcor) + abs(Ycur - Ycur)
            but this did not work out
            and the heuristic was not working at all.
            later had discussions with friends and found we need to use manhattan distance to find the distance between
            points and solve the problem. 
            heuristic , corner = min([(util.manhattanDistance(currentState, corner), corner) for corner in unvisitedCorner])
            Heuristic distance get added when agent moved forward with the cost in entire search

Question 7: i wasnt able to use position to form a better heuristic, but returned the length of food list which is total nmber
            of food left. it is admissable heuristic but not efficient for sure sunce i was able to score only 2/4

Question 8: for this problem, two methods are implemented, returning goal state for anyfoodsearchProblem, if the agent is in the
            spot where food is, the spot is the goal spot and 
            path to closest dot( which is food) used astar search to go the the closest dot.
            ///program uses dfs even when i ask astar search, why so???????


#multiagent implementaion:

question 1: Reflex Agent
	for this question, i took help from the class lecture mostly, but tried to understad the logic
        behind the code. I tried to make sure about the behavior of the pacman within various conditions,
        when integrating food pallets, adding ghosts, adding in the scared times for pacman to ear the ghost and 
        other properties which help make the evaluation function better.

Question 2: Minimax
       this Question was also based on the class lecture, which calculates the best action in the given depth
       of the pacman and the ghost. on this implementation the ghost stops at random position and when the ghost
       comes around it runs away, i didnt see the pacman wining for most of the parts
