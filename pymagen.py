#!/usr/bin/env python

from __future__ import division
import png
import random
import math
import sys
import copy


def add(x, y):
    return x + y


def sub(x, y):
    return x - y


def rsub(x, y):
    return y - x


def mod(x, y):
    return x % y if y != 0 else x


def mod2(x, y):
    return y % x if x != 0 else y


def mul(x, y):
    return x * y


def div(x, y):
    return x / y if y != 0 else x


def pow(x, y):
    try:
        return math.pow(x, y)
    except OverflowError:
        return 0
    except ValueError:
        return 0


def sinx(x, y):
    try:
        return math.sin(x / 100) * 255
    except ValuError:
        return 0


def siny(x, y):
    try:
        return math.sin(y / 100) * 255
    except ValuError:
        return 0


def sqrt(x, y):
    return math.sqrt(math.fabs(x))


def lt(x, y):
    return 255 if x < y else 0


def gt(x, y):
    return 0 if x < y else 255


ops = [add, sub, rsub, mod, mod2, mul, div, pow, sqrt, sinx, siny, lt, gt,
       max, min]


class Pymagen():
    def __init__(self, op=None, left=None, right=None, const=None):
        self.op = op
        self.left = left
        self.right = right
        self.const = const

    def apply_op(self, left, right, width, height):
        result = []
        for x in range(width):
            result.append([])
            for y in range(height):
                result[x].append(self.op(left[x][y] if left is not None else x,
                                         right[x][y] if right is not None else y))
        return result

    def resolve(self, width, height, array):
        if self.const is not None:
            return [[self.const for x in range(width)] for y in range(height)]
        left = self.left.resolve(width, height, array) if isinstance(self.left, Pymagen) else None
        right = self.right.resolve(width, height, array) if isinstance(self.right, Pymagen) else None
        return self.apply_op(left, right, width, height)

    def add_a_new_child(self):
        ptr = self
        while True:
            if random.randint(0, 1) == 0:
                op = Pymagen(op=random.choice(ops))
            else:
                op = Pymagen(const=random.uniform(0, 255))
            if random.randint(0, 1) == 0:
                if ptr.left == None:
                    ptr.left = op
                    return
                else:
                    ptr = ptr.left
            else:
                if ptr.right == None:
                    ptr.right = op
                    return
                else:
                    ptr = ptr.right

    def childs(self):
        to_explore = []
        to_explore.append(self)
        explored = []
        while len(to_explore) > 0:
            new_exploration = []
            for tree in to_explore:
                if isinstance(tree.left, Pymagen):
                    new_exploration.append(tree.left)
                if isinstance(tree.right, Pymagen):
                    new_exploration.append(tree.right)
                explored.append(tree)
            to_explore = new_exploration
        return explored

    def edit_a_child(self):
        target = random.choice(self.childs())
        if random.randint(0, 20) == 0:
            target.const = random.uniform(0, 255)
            target.op = None
        else:
            target.const = None
            target.op = random.choice(ops)

    def edit_a_child_constant(self):
        targets = [c for c in self.childs() if c.const is not None]
        if len(targets) == 0:
            return
        target = random.choice(targets)
        if target is not None:
            target.const = random.uniform(0, 255)

    def evolve(self):
        if random.randint(0, 5) > 0:
            self.add_a_new_child()
        for i in self.childs():
            if random.randint(0, 3) > 2:
                self.edit_a_child()
                self.edit_a_child_constant()

    def __str__(self):
        if self.const is not None:
            return "%.2f" % self.const
        return "%s(%s, %s)" % (self.op.__name__,
                               self.left if self.left is not None else "x",
                               self.right if self.right is not None else "y")

    def truncate(self, x):
        return int(max(0, min(255, x)))


def tree2array(width, height, tree):
    array = [[0 for x in range(width)] for y in range(height)]
    array = tree.resolve(width, height, array)
    return [[tree.truncate(array[x][y])
             for x in range(width)]
            for y in range(height)]


trees = [Pymagen(random.choice(ops)) for _ in range(10)]

while True:
    for i in range(10):
        if i > 0:
            trees[i].evolve()
        print "%i: %s" % (i, trees[i])
        print "Calculating ..."
        array = tree2array(255, 255, trees[i])
        print "Rendering ..."
        png.from_array(array, 'L').save('%i.png' % i)
        print "Done"
    print "Which one ?"
    while True:
        try:
            who = int(sys.stdin.readline())
            for x in range(10):
                trees[x] = copy.deepcopy(trees[who])
        except ValueError:
            print "What !?"
        else:
            break
