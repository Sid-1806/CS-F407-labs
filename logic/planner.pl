% Task 6: warehouse connectivity facts and rule
connected(a,b).
connected(b,a).
connected(b,c).
connected(c,b).

can_move(X,Y) :-
    connected(X,Y).

% Task 7: verifying a proposed plan of Move actions
valid_move(X,Y) :-
    connected(X,Y).

% Example queries to run at the Prolog prompt:
%
% Task 6:
% ?- can_move(a,b).      % expect: true
% ?- can_move(a,c).      % expect: false
%
% Task 7:
% ?- valid_move(a,b).    % expect: true
% ?- valid_move(b,c).    % expect: true
% ?- valid_move(a,c).    % expect: false  (a and c are not directly connected)
