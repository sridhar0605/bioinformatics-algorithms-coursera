#!/usr/bin/env python
'''
A solution to a programming assignment for the Bioinformatics Algorithms (Part 1) on Coursera.
The associated textbook is Bioinformatics Algorithms: An Active-Learning Approach by Phillip Compeau & Pavel Pevzner.
The course is run on Coursera and the assignments and textbook are hosted on Stepic

Problem Title: Alignment with Affine Gap Penalties Problem
Assignment #: 07
Problem ID: D
URL: https://stepic.org/Bioinformatics-Algorithms-2/Penalizing-Insertions-and-Deletions-in-Sequence-Alignments-249/step/8
'''

from scripts import BLOSUM62


def global_alignment_affine_gap_penalty(v, w, scoring_matrix, sigma, epsilon):
    '''Returns the global alignment score of v and w with constant gap peantaly sigma subject to the scoring_matrix.'''
    # Initialize the matrices.
    S = [[[0 for j in xrange(len(w)+1)] for i in xrange(len(v)+1)] for k in xrange(3)]
    backtrack = [[[0 for j in xrange(len(w)+1)] for i in xrange(len(v)+1)] for k in xrange(3)]

    # Initialize the edges with the given penalties.
    for i in xrange(1, len(v)+1):
        S[0][i][0] = -sigma - (i-1)*epsilon
        S[1][i][0] = -sigma - (i-1)*epsilon
        S[2][i][0] = -10*sigma
    for j in xrange(1, len(w)+1):
        S[2][0][j] = -sigma - (j-1)*epsilon
        S[1][0][j] = -sigma - (j-1)*epsilon
        S[0][0][j] = -10*sigma

    # Fill in the scores for the lower, middle, upper, and backtrack matrices.
    for i in xrange(1, len(v)+1):
        for j in xrange(1, len(w)+1):
            lower_scores = [S[0][i-1][j] - epsilon, S[1][i-1][j] - sigma]
            S[0][i][j] = max(lower_scores)
            backtrack[0][i][j] = lower_scores.index(S[0][i][j])

            upper_scores = [S[2][i][j-1] - epsilon, S[1][i][j-1] - sigma]
            S[2][i][j] = max(upper_scores)
            backtrack[2][i][j] = upper_scores.index(S[2][i][j])

            middle_scores = [S[0][i][j], S[1][i-1][j-1] + scoring_matrix[v[i-1], w[j-1]], S[2][i][j]]
            S[1][i][j] = max(middle_scores)
            backtrack[1][i][j] = middle_scores.index(S[1][i][j])

   # Initialize the values of i, j and the aligned sequences.
    i,j = len(v), len(w)
    v_aligned, w_aligned = v, w

    # Get the maximum score, and the corresponding backtrack starting position.
    matrix_scores = [S[0][i][j], S[1][i][j], S[2][i][j]]
    max_score = max(matrix_scores)
    backtrack_matrix = matrix_scores.index(max_score)

    # Quick lambda function to insert indels.
    insert_indel = lambda word, i: word[:i] + '-' + word[i:]

    # Backtrack to the edge of the matrix starting bottom right.
    while i*j != 0:
        if backtrack_matrix == 0:  # Lower backtrack matrix conditions.
            if backtrack[0][i][j] == 1:
                backtrack_matrix = 1
            i -= 1
            w_aligned = insert_indel(w_aligned, j)

        elif backtrack_matrix == 1:  # Middle backtrack matrix conditions.
            if backtrack[1][i][j] == 0:
                backtrack_matrix = 0
            elif backtrack[1][i][j] == 2:
                backtrack_matrix = 2
            else:
                i -= 1
                j -= 1

        else:  # Upper backtrack matrix conditions.
            if backtrack[2][i][j] == 1:
                backtrack_matrix = 1
            j -= 1
            v_aligned = insert_indel(v_aligned, i)

    # Prepend the necessary preceeding indels to get to (0,0).
    for _ in xrange(i):
        w_aligned = insert_indel(w_aligned, 0)
    for _ in xrange(j):
        v_aligned = insert_indel(v_aligned, 0)

    return str(max_score), v_aligned, w_aligned


def main():
    '''Main call. Reads, runs, and saves problem specific data.'''
    # Read the input data.
    with open('data/stepic_7d.txt') as input_data:
        protein1, protein2 = [line.strip() for line in input_data.readlines()]

    # Get the alignment score.
    score = global_alignment_affine_gap_penalty(protein1, protein2, BLOSUM62(), 11, 1)

    # Print and save the answer.
    print '\n'.join(score)
    with open('output/Assignment_07D.txt', 'w') as output_data:
        output_data.write('\n'.join(score))

if __name__ == '__main__':
    main()
