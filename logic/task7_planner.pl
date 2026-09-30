% Task 7: Using Prolog to Check a Proposed Plan
% Extends the warehouse connectivity knowledge base from Task 6.

connected(a,b).
connected(b,a).
connected(b,c).
connected(c,b).

valid_move(X,Y) :-
    connected(X,Y).

% Proposed plan from the Python planner: Move(a,b), Move(b,c)
% Queries to run at the Prolog prompt:
% ?- valid_move(a,b).
% ?- valid_move(b,c).
% ?- valid_move(a,c).
%
% Challenge: check whether Move(a,c) is supported by the warehouse knowledge:
% ?- valid_move(a,c).
