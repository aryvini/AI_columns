# AI Columns

This project try to build an ML model to help the dimensioning of RC columns by giving the best estimatives based on a amount of solutions provided by PFOC.

Differently from PFOC, that evaluates the mathematics of the solution, AI Columns aim to build a ML estimator based on the solutions, thus, making it more quickly than the PFOC it self, since it iterates under a huge amount of possibilities. 
When the model is trained, a in few seconds is possible to estimate the best cross section.

**NOTE** that AI_columns only give the best alternative, but the proof of the cross section must be done anyway, the goal here is to reduce time by not testing other options that are clearly not possible.


# About PFOC

PFOC is a [project](https://github.com/DanielDgrossmann/PFOC) hosted on github, developed by [Daniel Grossmann](https://github.com/DanielDgrossmann/PFOC) to optimize the cross section of columns under oblique loads, e.g Moment loads on both axis and axial load. 
In order to do this, a series of parameters needs to be inputed, such as cost of materials (concrete and rebar). 

The algorithms iterates over all possibilities of cross section (intergers) and return the most cost effience cross section.




