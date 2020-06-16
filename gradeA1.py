import os
import sys
import argparse
import re

def grade_submission_a1_t4_match(match, case):
    avgwait = []
    avgwait.append(float(match.group(1)))
    avgwait.append(float(match.group(3)))
    avgwait.append(float(match.group(5)))
    avgwait.append(float(match.group(7)))
    maxwait = []
    maxwait.append(float(match.group(2)))
    maxwait.append(float(match.group(4)))
    maxwait.append(float(match.group(6)))
    maxwait.append(float(match.group(8)))

    avgall = float(match.group(9))
    total = float(match.group(10))

    res = 0
    comment = []
    if case == 1 or case == 2:
        res = 2
        for wait in avgwait:
            if wait > 0:
                res = 0
                comment.append('The average waiting time should be zero for all directions.')
                break
    elif case == 3:
        if avgall > 0.01:
            res = 0
            comment.append('The overall average waiting time should be 10 milliseconds or less.')
        else:
            res = 3
    elif case == 4:
        if avgall > 0.01:
            res = 0
            comment.append('The overall average waiting time should be 10 milliseconds or less.')
        else:
            res = 2
    elif case == 5:
        res = 3
        if total > 6:
            res -= 1.5
            comment.append('The total simulation time should be less than 6 seconds.')
        for wait in maxwait:
            if wait > 0.025:
                res -= 1.5
                comment.append('The maximum waiting time for each direction should be less than 15ms + 10ms = 25ms.')
                break
    elif case == 6:
        res = 2
        if total > 6:
            res -= 1
            comment.append('The total simulation time should be less than 6 seconds.')
        for wait in maxwait:
            if wait > 0.025:
                res -= 1
                comment.append('The maximum waiting time for each direction should be less than 15ms + 10ms = 25ms.')
                break
    elif case == 7:
        res = 3
        if total > 5:
            res -= 1.5
            comment.append('The total simulation time should be less than 5 seconds.')
        for wait in maxwait:
            if wait > 0.065:
                res -= 0.75
                comment.append('The maximum waiting time for each direction should be less than 55ms + 10ms = 65ms.')
                break
        for wait in avgwait:
            if wait - avgall > 0.01 or avgall - wait > 0.01:
                res -= 0.75
                comment.append('The average waiting time for each direction should be within 10ms of the overall average waiting time.')
                break
    elif case == 8:
        res = 2
        if total > 5:
            res -= 1
            comment.append('The total simulation time should be less than 5 seconds.')
        for wait in maxwait:
            if wait > 0.065:
                res -= 1
                comment.append('The maximum waiting time for each direction should be less than 55ms + 10ms = 65ms.')
                break
    elif case == 9:
        res = 3
        if total > 4:
            res -= 1.5
            comment.append('The total simulation time should be less than 4 seconds.')
        for wait in maxwait:
            if wait > 0.105:
                res -= 0.75
                comment.append('The maximum waiting time for each direction should be less than 95ms + 10ms = 105ms.')
                break
        for wait in avgwait:
            if wait - avgall > 0.01 or avgall - wait > 0.01:
                res -= 0.75
                comment.append('The average waiting time for each direction should be within 10ms of the overall average waiting time.')
                break
    elif case == 10:
        res = 2
        if total > 4:
            res -= 1
            comment.append('The total simulation time should be less than 4 seconds.')
        for wait in maxwait:
            if wait > 0.105:
                res -= 1
                comment.append('The maximum waiting time for each direction should be less than 95ms + 10ms = 105ms.')
                break    
    else:
        comment.append('Illegel test case')
        res = 0

    return res, comment

def grade_submission_a1_t4(folder):
    logfile = os.path.join(folder, 'runTests.log')
    if not os.path.isfile(logfile):
        return 0, ['Grading log file not found. Is this submission empty?']

    with open(logfile, 'r') as fin:
        text = fin.read(4 * 1048576)    # should be large enough

    anchor = [
        'sp3 1 150 1 1 0',
        'sp3 1 150 1 1 1',
        'sp3 5 100 10 1 0',
        'sp3 5 100 10 1 1',
        'sp3 2 300 0 1 0',
        'sp3 2 300 0 1 1',
        'sp3 6 100 0 1 0',
        'sp3 6 100 0 1 1',
        'sp3 10 80 0 1 0',
        'sp3 10 80 0 1 1'
    ]

    pattern = re.compile(r'^N:[^v]*vehicles, average wait ([\d\.]*) seconds, max wait ([\d\.]*) seconds$\n^E:[^v]*vehicles, average wait ([\d\.]*) seconds, max wait ([\d\.]*) seconds$\nS:[^v]*vehicles, average wait ([\d\.]*) seconds, max wait ([\d\.]*) seconds$\nW:[^v]*vehicles, average wait ([\d\.]*) seconds, max wait ([\d\.]*) seconds$\nall:[^v]*vehicles, average ([\d\.]*) seconds waiting$\nSimulation: ([\d\.]*) seconds,.*$\n', re.MULTILINE)

    mark_acc = 0
    comments = []

    for i in range(0, len(anchor)):
        start = text.find(anchor[i])
        if start == -1:
            comments.append('Failed to locate anchor ' + str(i+1))
            continue
        if i+1 < len(anchor):
            end = text.find(anchor[i+1])
        else:
            end = len(text)

        match = pattern.search(text, start, end)
        if not match:
            comments.append('Output not found for test case ' + str(i+1))
            continue
        if match.lastindex < 10:
            comments.append('Output ill-formated for test case ' + str(i+1))
            continue

        mark, comment_list = grade_submission_a1_t4_match(match, i+1)
        if mark < 0:
            print('ERROR')
            sys.exit(1)
        
        mark_acc += mark
        for comment in comment_list:
            comments.append('Test case ' + str(i+1) + ': ' + comment)

    return mark_acc, comments

def main(args):
    submission_folder = os.path.abspath(args.folder)
    folders = os.listdir(submission_folder)
    folders.sort()
    for folder in folders:
        submission_name = folder
        fullpath = os.path.join(submission_folder, folder)
        if not os.path.isdir(fullpath):
            continue
        
        score, comments = grade_submission_a1_t4(fullpath)

        print('========================')
        print(submission_name)
        print('Score: ' + str(score))
        print('Comments: ')
        for comment in comments:
            print(comment)
        print('\n\n\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This is a script to grade CS350 A1 Test 4 at a university. Apparently most people here prefer to grade with their naked eyes. For bug reports, please send them to duanqn_own_1 (AT) yeah.net')

    parser.add_argument('-p', '--submission-folder', metavar='PATH', type=str, required=False, default='.', dest='folder', help='This is the path to the submission folder. All submissions should be under this folder.')

    args = parser.parse_args()
    main(args)