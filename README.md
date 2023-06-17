# A* Pathfinder

This program simulates a robot moving through a 2D grid containing randomly generated obstacles in order to reach some end goal. I used the A* pathfinding algorithm to compute the shortest path from the starting point to the ending point, and then visually simulated the robot moving through the grid using Pygame.

## Demo

https://github.com/LucasStevenson/aStar-Pathfinder/assets/45473315/79795b52-5392-45ec-958a-eb9d05283615

## Project Reflection

### Performance

I measured the performance of this algorithm based on the number of cells in the grid that get visited. The less, the better, since that means are doing less work and computation.

For testing purposes, I modified my code a little so that visited cells are colored turquoise. Here's the results.

With a random seed of 100 (this is relevant in generating the obstacles)

![image](https://i.imgur.com/IVSJE6f.png)

Looks pretty good. Cells that clearly move further away from the end goal, which is at the bottom right of the screen, are not explored by the A* algorithm.

An important thing to note is that **the placement of obstacles makes a big difference in how many cells get checked**.

To prove this, let's change the random seed to 10.

![image](https://i.imgur.com/ECEJseS.png)

Relative to the previous picture, we can see a lot more cells were checked and visited. Still though, paths that very obviously moved away from the end goal were not explored, which is good. The big question still remains, how come in the first case A* did a lot less work than in the second?

##### Obstacles, start, and end placements

As noted before, the placement of obstacles makes a big difference in how many cells get checked. Another thing that is important is the placement of the start and end points.

1. Obstacle placement

Obstacles play a big role in things because they quite literally change the landscape of the grid and oftentimes force the robot to move a certain way/go to certain places. Sometimes, this works in our favor. For example, if an obstacle forces the robot to move to the right, closer to the end goal, then (unless we're forced to by other obstacles) we have no real reason to move back to the left since that brings us further from the goal.

2. Start and end point placement

The positioning of both the start and end points also make a difference in how much work the algorithm does. This intuitively makes sense, but I thought it was still worth pointing out. In my testing, I put these two points in completely opposite corners, so this factor remained constant in the two images above.

So to answer the question of why less work was done in the first image compared to the second, it boils down to obstacle placement. In the first image, obstacles were generated in such a way where there was a more direct and forcing path. On the other hand, the obstacles in the second image allowed for a lot more paths to be explored since the movement of the robot was a lot more free and there were many paths that could potentially be the shortest one.

### Challenges

The main challenge I had in this project was in the analysis of the A* code I wrote (this was before I ran the tests above).

I kept on wondering whether or not it was any more effective than a simple BFS. Naturally, I felt like it should be better since it has the added heuristic that serves the purpose of prioritizing nodes closer to the end goal. The thing is, the scenario I drew out and manually simulated the algorithm on happened to be the one where A* does behave like BFS. This case is when there are no obstacles and the starting point is at the top left of the screen and the ending is at the bottom right. 

> The reason this specific scenario results in A* behaving like BFS is because from the starting point, every step we take brings us closer to the end node. The g_score will increase by one every neighbor we visit, and the h_score will decrease by 1. This means the f_score of every single node will always be the same.

After thinking about it a little longer, I realized that A* is indeed more efficient than a simple BFS/Dijkstra. I visually showed it via highlighting the cells that the algorithm visits, as seen in the images above.
