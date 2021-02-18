# -*- coding: utf-8 -*-

# SPDX-License-Identifier: MIT
# Copyright © 2021 André Santos


###############################################################################
# Imports
###############################################################################

from __future__ import print_function

from .rendering import TemplateRenderer


###############################################################################
# Constants
###############################################################################

EMPTY_DICT = {}

INF = float("inf")


################################################################################
# Parsing
################################################################################

def parse_single_property(arg):
    return

def parse_property_file(text):
    return []


################################################################################
# Generation
################################################################################

def gen_monitor_nodes(props, output_dir):
    pass

def get_imports():
    return set()

def render_rv_common():
    return ""

def render_monitor(prop):
    # depends on stuff from rv_common
    return ""


################################################################################
# Entry Point
################################################################################

# http://wiki.ros.org/rospy_tutorials/Tutorials/Makefile
# https://answers.ros.org/question/323563/ros-1-correct-way-to-declare-python-dependencies/
# https://github.com/ros/rosdistro/blob/master/rosdep/python.yaml

# tool [-o <dir>] [-p] [-s <yaml_file>] [-t <yaml_file>] [-i] <arg1> <arg2> ...

# -o:   output directory for generated files
# -p:   positional args are properties, not HPL files
# -t:   [not needed for RV] type token dict file {msg type name -> {field: type}}
# -s:   signature dict file {ros name -> msg type name}
# -i:   interactive mode, ask for missing ros names
# -r:   allow use of rospy to build type tokens

def main(args):
    output_dir = args.output_dir
    is_property = args.input_property
    if is_property:
        for arg in args.args: # positional args, at least 1
            prop = parse_single_property(arg)
    else: # is file
        for arg in args.args:
            with open(arg, "r") as f:
                text = f.read().strip()
            props = parse_property_file(text)
    gen_monitor_nodes(props, output_dir)



ABSENCE_EXAMPLES = [
    '''
    # id: p1
    # title: "My First Property"
    # description: "This is a test property to be transformed into a monitor."
    globally: no /ns/topic {data > 0}
    ''',

    'globally: no /ns/topic {data > 0} within 100 ms',

    'after /p: no /b {data > 0} within 100 ms',

    'after /p as P: no /b {data > @P.data}',

    'until /q {phi}: no /b {data > 0} within 100 ms',

    'after /p as P until /q {phi and (not @P.psi)}: no /b {forall i in array: array[@i] > 0}',

    'after /p as P until /q {phi and (not @P.psi)}: no /b {exists i in [1 to 4]: array[@i] > 0} within 1 s',

    'globally: no (/b1 {data > 0} or /b2 {data < 0})  within 100 ms',

    'after /b: no /b {3 * data**2 > 0}',

    'after (/p or /q or /b): no /b {data in {1,2,3}}',
]

EXISTENCE_EXAMPLES = [e.replace(' no ', ' some ') for e in ABSENCE_EXAMPLES]

PRECEDENCE_EXAMPLES = [
    'globally: /b requires /a',

    'globally: /b requires /a within 100 ms',

    'globally: /b {data > 0} requires /a {data < 0}',

    'globally: /b {data > 0} requires /a {data < 0} within 100 ms',

    'globally: (/b1 {data > 0} or /b2 {data < 0}) requires /a',

    'globally: (/b1 {data > 0} or /b2 {data < 0}) requires /a within 100 ms',

    'globally: /b requires (/a1 {data > 0} or /a2 {data < 0})',

    'globally: /b requires (/a1 {data > 0} or /a2 {data < 0}) within 100 ms',

    'globally: /b requires /b within 100 ms',

    'globally: /b requires /b {data > 0} within 100 ms',

    'globally: /b {data > 0} requires /b within 100 ms',

    'after /p: /b requires /a',

    'after /p: /b requires /a within 100 ms',

    'after /p {phi implies psi}: /b {data > 0} requires /a {data < 0}',

    'after /p {phi iff psi}: /b {data > 0} requires /a {data < 0} within 100 ms',

    'after /p: (/b1 {data > 0} or /b2 {data < 0}) requires /a',

    'after /p: (/b1 {data > 0} or /b2 {data < 0}) requires /a within 100 ms',

    'after /p: /b requires (/a1 {data > 0} or /a2 {data < 0})',

    'after /p: /b requires (/a1 {data > 0} or /a2 {data < 0}) within 100 ms',

    'after (/p1 {x in {1,2,3}} or /p2 {y in ![0 to 10]!}): /b requires /a',

    'after (/p1 {x in {1,2,3}} or /p2 {y in ![0 to 10]!}): /b requires /a within 100 ms',

    'after /b: /b requires /a within 100 ms',

    'after /a: /b requires /a within 100 ms',

    'after /b: /b requires /b within 100 ms',

    'until /q {phi}: /b {psi} requires /a {omega}',

    'until /q {phi}: /b {psi} requires /a {omega} within 100 ms',

    'until /q: (/b1 {phi} or /b2 {psi}) requires /a',

    'until (/q1 or /q2): /b requires /a',

    'until /b: /b requires /a',

    'until /a: /b requires /a',

    'after /p {phi} until /q {psi}: /b {beta} requires /a {alpha}',

    'after /p {phi} until /q {psi}: /b {beta} requires /a {alpha} within 100 ms',

    'after /p until /q: (/b1 {beta} or /b2 {beta}) requires /a',

    'after /p until (/q1 or /q2): /b requires /a',

    'after (/p or /q) until /q: /b requires /a',

    'after /b until /q: /b requires /a',

    'after /p until /a: /b requires /a',
]

PRECEDENCE_REF_EXAMPLES = [
    'globally: /b as B requires /a {data < @B.data}',

    'globally: /b as B {data > 0} requires /a {data < @B.data} within 100 ms',

    'globally: /b as B {x > 0} requires /a {x < 0 and y < @B.y}',

    'globally: /b as B {x > 0} requires /a {forall i in array: (array[@i] > 0 and array[@i] < @B.x)} within 100 ms',

    'after /p as P until /q {x > @P.x}: /b as B {x = @P.x} requires (/a1 {not (a < 0 or a > @B.b)} or /a2 {a in {0, @B.b}}) within 100 ms'
]

RESPONSE_EXAMPLES = [
    'globally: /a causes /b',

    'globally: /a causes /b within 100 ms',

    'globally: /a {data > 0} causes /b {data < 0}',

    'globally: /a {data > 0} causes /b {data < 0} within 100 ms',

    'globally: (/a1 {data > 0} or /a2 {data < 0}) causes /b within 100 ms',

    'globally: /a causes (/b1 {data > 0} or /b2 {data < 0}) within 100 ms',

    'after /p: /a causes /b within 100 ms',

    'after /p {phi}: /a {data > 0} causes /b {data < 0} within 100 ms',

    'until /q: /a {phi} causes /b {psi} within 100 ms',

    'until /b: /a causes /b within 100 ms',

    'until /a: /a causes /b within 100 ms',

    'after /p {phi} until /q {psi}: /a {alpha} causes /b {beta}',

    'after /p {phi} until /q {psi}: /a {alpha} causes /b {beta} within 100 ms',

    'globally: /a as A causes /b {x < @A.x}',

    'globally: /a as A {x > 0} causes /b {x < @A.x} within 100 ms',

    'globally: /a as A {x > 0} causes (/b1 {x < @A.x} or /b2 {y < @A.y}) within 100 ms',

    'after /p as P until /q {x > @P.x}: /a as A {x = @P.x} causes (/b1 {x < @A.x + @P.x} or /b2 {x in {@P.x, @A.x}}) within 100 ms'
]

PREVENTION_EXAMPLES = [p.replace('causes', 'forbids') for p in RESPONSE_EXAMPLES]


AGROB_EXAMPLES = [
'''
# id: unused_topics
# title: "Unused topics"
# description: "No messages should be published on these topics."
globally:
    no (
        /Agrob_path/plan_local
        or
        /TrajectoryControlCommand
    )
''',

'''
# id: valid_states
# title: "Valid States"
# description: "Enumeration of all valid states in /Agrob_path/agrob_pp/state."
globally:
    no /Agrob_path/agrob_pp/state {
        not data in {
            "WAITING_FOR_MAP", "LOADING_MAP", "READY_TO_PLAN", "PLANNING",
            "PLANNING_SUCCESSFUL", "PLANNING_FAILED", "OFFLINE_DOCK_PLAN_MODE"
        }
    }
''',

'''
# id: valid_initial_poses
# title: "Valid Initial Poses"
# description: "Conditions that apply to all valid initial poses."
after /map as M:
    no /Agrob_path/initialPose {
        ( pose.pose.position.x < @M.info.origin.position.x )
        or
        ( pose.pose.position.x > (@M.info.width * @M.info.resolution + @M.info.origin.position.x) )
        or
        ( pose.pose.position.y < @M.info.origin.position.y )
        or
        ( pose.pose.position.y > (@M.info.height * @M.info.resolution + @M.info.origin.position.y) )
        or
        ( @M.data[int((pose.pose.position.y + @M.info.origin.position.y) * @M.info.width
                  + (pose.pose.position.x + @M.info.origin.position.x))] != 0 )
    }
''',

'''
# id: valid_goal_poses
# title: "Valid Goal Poses"
# description: "Conditions that apply to all valid goal poses."
after /map as M:
    no /Agrob_path/goalPose {
        ( pose.position.x < @M.info.origin.position.x )
        or
        ( pose.position.x > (@M.info.width * @M.info.resolution + @M.info.origin.position.x) )
        or
        ( pose.position.y < @M.info.origin.position.y )
        or
        ( pose.position.y > (@M.info.height * @M.info.resolution + @M.info.origin.position.y) )
        or
        ( @M.data[int((pose.position.y + @M.info.origin.position.y) * @M.info.width
                  + (pose.position.x + @M.info.origin.position.x))] != 0 )
    }
''',

'''
# id: valid_plan_pub_positions
# title: "Valid Positions in Plans"
# description: "Conditions that apply to all positions of published plans."
after /map as M:
    no /Agrob_path/plan_pub {
        exists i in poses: (
            ( poses[@i].pose.position.x < @M.info.origin.position.x )
            or
            ( poses[@i].pose.position.x > (@M.info.width * @M.info.resolution + @M.info.origin.position.x) )
            or
            ( poses[@i].pose.position.y < @M.info.origin.position.y )
            or
            ( poses[@i].pose.position.y > (@M.info.height * @M.info.resolution + @M.info.origin.position.y) )
            or
            ( @M.data[int((poses[@i].pose.position.y + @M.info.origin.position.y) * @M.info.width
                      + (poses[@i].pose.position.x + @M.info.origin.position.x))] != 0 )
        )
    }
''',

'''
# id: valid_plan_pub_distance
# title: "Valid Distances in Plans"
# description: "FIXME Between two consecutive poses, the distance should not exceed 3 times the map's resolution."
after /map as M:
    no /Agrob_path/plan_pub {
        exists i in [0 to (len(poses) - 2)]: (
            ( abs(poses[@i].pose.position.x - poses[@i+1].pose.position.x)
                < (2 * @M.info.resolution) )
            or
            ( abs(poses[@i].pose.position.x - poses[@i+1].pose.position.x)
                > (3 * @M.info.resolution) )
            or
            ( abs(poses[@i].pose.position.y - poses[@i+1].pose.position.y)
                < (2 * @M.info.resolution) )
            or
            ( abs(poses[@i].pose.position.y - poses[@i+1].pose.position.y)
                > (3 * @M.info.resolution) )
        )
    }
''',

'''
# id: valid_plan_pub_angles
# title: "Valid Orientations in Plans"
# description: "Between two consecutive poses, the difference of orientations should not exceed 22.5 degrees."
globally:
    no /Agrob_path/plan_pub {
        exists i in [0 to (len(poses) - 2)]: (
            deg(abs(
                yaw(poses[@i+1].pose.orientation)
                - yaw(poses[@i].pose.orientation)
            )) > 22.5
        )
    }
''',

'''
# id: valid_cell_markers
# title: "Valid Cell Markers"
# description: "[Type Invariant] Only valid cell markers are produced."
globally:
    no /Agrob_path/cells_marker_array {
        exists i in markers: (
            (not markers[@i].type in [0 to 11])
            or
            (not markers[@i].action in {0, 2, 3})
            or
            (markers[@i].text != "" and markers[@i].type != 9)
            or
            (markers[@i].mesh_resource != "" and markers[@i].type != 10)
            or
            (markers[@i].mesh_use_embedded_materials and markers[@i].type != 10)
        )
    }
''',

'''
# id: initial_state
# title: "Initial State"
# description: "WAITING_FOR_MAP is the initial state."
until /Agrob_path/agrob_pp/state { data = "WAITING_FOR_MAP" }:
    no /Agrob_path/agrob_pp/state
''',

'''
# id: goto_waiting_for_map
# title: "WAITING_FOR_MAP is Reachable"
# description: "The WAITING_FOR_MAP state is eventually reached."
globally:
    some /Agrob_path/agrob_pp/state { data = "WAITING_FOR_MAP" }
    within 10 s
''',

'''
# id: until_map
# title: "No Plan Without a Map"
# description: "Cannot start planning until a map is published."
until /map:
    no (
        /Agrob_path/agrob_pp/state { data != "WAITING_FOR_MAP" }
        or
        /Agrob_path/plan_pub
        or
        /Paramatric_Path
        or
        /Path
        or
        /inflation_cloud
    )
''',

'''
# id: some_map
# title: "There is a Map"
# description: "Eventually a map is published."
globally: some /map within 300 s
''',

'''
# id: goto_loading_map
# title: "LOADING_MAP is Reachable"
# description: "After receiving a map it enters the LOADING_MAP state."
after /map:
    some /Agrob_path/agrob_pp/state { data = "LOADING_MAP" }
    within 10 s
''',

'''
# id: second_state
# title: "Second State"
# description: "LOADING_MAP is the second state."
until /Agrob_path/agrob_pp/state { data = "LOADING_MAP" }:
    no /Agrob_path/agrob_pp/state { data != "WAITING_FOR_MAP" }
''',

'''
# id: goto_ready_to_plan
# title: "READY_TO_PLAN is Reachable"
# description: "After loading the map it enters the READY_TO_PLAN state."
after /Agrob_path/agrob_pp/state { data = "LOADING_MAP" }:
    some /Agrob_path/agrob_pp/state { data = "READY_TO_PLAN" }
    within 240 s
''',

'''
# id: third_state
# title: "Third State"
# description: "READY_TO_PLAN is the third state."
until /Agrob_path/agrob_pp/state { data = "READY_TO_PLAN" }:
    no /Agrob_path/agrob_pp/state {
        not data in {"WAITING_FOR_MAP", "LOADING_MAP"}
    }
''',

'''
# id: planning_loop
# title: "Planning Loop"
# description: "READY_TO_PLAN starts the planning loop."
after /Agrob_path/agrob_pp/state { data = "READY_TO_PLAN" }:
    no /Agrob_path/agrob_pp/state {
        not data in {
            "READY_TO_PLAN", "PLANNING",
            "PLANNING_SUCCESSFUL", "PLANNING_FAILED"
        }
    }
''',

'''
# id: planning_after_ready
# title: "Only PLANNING After READY_TO_PLAN"
# description: "PLANNING is the state following READY_TO_PLAN."
after /Agrob_path/agrob_pp/state { data = "READY_TO_PLAN" }
until /Agrob_path/agrob_pp/state { data = "PLANNING" }:
    no /Agrob_path/agrob_pp/state
''',

'''
# id: result_after_planning
# title: "Only Success or Failure After PLANNING"
# description: "PLANNING_SUCCESSFUL or PLANNING_FAILED are the two possible states following PLANNING."
after /Agrob_path/agrob_pp/state { data = "PLANNING" }
until /Agrob_path/agrob_pp/state {
    data = "PLANNING_SUCCESSFUL" or data = "PLANNING_FAILED"
}:
    no /Agrob_path/agrob_pp/state
''',

'''
# id: ready_after_result
# title: "Only READY_TO_PLAN After Success or Failure"
# description: "PLANNING_SUCCESSFUL or PLANNING_FAILED can only go back to READY_TO_PLAN."
after /Agrob_path/agrob_pp/state {
    data = "PLANNING_SUCCESSFUL" or data = "PLANNING_FAILED"
}
until /Agrob_path/agrob_pp/state { data = "READY_TO_PLAN" }:
    no /Agrob_path/agrob_pp/state
''',

'''
# id: some_goal
# title: "There is a Goal Pose"
# description: "When READY_TO_PLAN, eventually a goal pose is published."
after /Agrob_path/agrob_pp/state { data = "READY_TO_PLAN" }
until /Agrob_path/agrob_pp/state { data = "PLANNING" }:
    some /Agrob_path/goalPose
    within 400 ms
''',

'''
# id: some_pose
# title: "There is an Initial Pose"
# description: "When READY_TO_PLAN, eventually an initial pose is published."
after /Agrob_path/agrob_pp/state { data = "READY_TO_PLAN" }
until /Agrob_path/agrob_pp/state { data = "PLANNING" }:
    some /Agrob_path/initialPose
    within 400 ms
''',

'''
# id: planning_requires_goal
# title: "PLANNING Requires a Goal Pose"
# description: "No transition to PLANNING before publishing a goal pose."
after /Agrob_path/agrob_pp/state { data = "READY_TO_PLAN" }
until /Agrob_path/agrob_pp/state {
    data = "PLANNING_SUCCESSFUL" or data = "PLANNING_FAILED"
}:
    /Agrob_path/agrob_pp/state { data = "PLANNING" }
    requires /Agrob_path/goalPose
''',

'''
# id: planning_requires_pose
# title: "PLANNING Requires an Initial Pose"
# description: "No transition to PLANNING before publishing an initial pose."
after /Agrob_path/agrob_pp/state { data = "READY_TO_PLAN" }
until /Agrob_path/agrob_pp/state {
    data = "PLANNING_SUCCESSFUL" or data = "PLANNING_FAILED"
}:
    /Agrob_path/agrob_pp/state { data = "PLANNING" }
    requires /Agrob_path/initialPose
''',

'''
# id: goto_planning
# title: "Poses Lead To PLANNING"
# description: "A goal pose eventually leads to a transition to PLANNING."
after /Agrob_path/agrob_pp/state { data = "READY_TO_PLAN" }
until /Agrob_path/agrob_pp/state {
    data = "PLANNING_SUCCESSFUL" or data = "PLANNING_FAILED"
}:
    /Agrob_path/goalPose
    causes /Agrob_path/agrob_pp/state { data = "PLANNING" }
    within 1 s
''',

'''
# id: spurious_plans
# title: "No Plans Before PLANNING"
# description: "No plans are published before the first PLANNING state."
until /Agrob_path/agrob_pp/state { data = "PLANNING" }:
    no (
        /Agrob_path/plan_pub
        or
        /Paramatric_Path
        or
        /Path
    )
''',

'''
# id: plan_requires_success
# title: "Plan Requires PLANNING_SUCCESSFUL"
# description: "Cannot publish a plan without visiting PLANNING_SUCCESSFUL."
after /Agrob_path/agrob_pp/state { data = "PLANNING" }
until /Agrob_path/agrob_pp/state { data = "READY_TO_PLAN" }:
    /Agrob_path/plan_pub
    requires /Agrob_path/agrob_pp/state { data = "PLANNING_SUCCESSFUL" }
''',

'''
# id: goto_success_or_failure
# title: "PLANNING_SUCCESSFUL or PLANNING_FAILED are Reachable"
# description: "A transition from PLANNING to PLANNING_SUCCESSFUL or PLANNING_FAILED eventually happens."
after /Agrob_path/agrob_pp/state { data = "PLANNING" }
until /Agrob_path/agrob_pp/state { data = "READY_TO_PLAN" }:
    some /Agrob_path/agrob_pp/state {
        data = "PLANNING_SUCCESSFUL" or data = "PLANNING_FAILED"
    }
    within 60 s
''',

'''
# id: success_plan
# title: "PLANNING_SUCCESSFUL Produces a Plan"
# description: "Entering the PLANNING_SUCCESSFUL state leads to the publication of a plan."
after /Agrob_path/agrob_pp/state { data = "PLANNING" }
until /Agrob_path/agrob_pp/state { data = "READY_TO_PLAN" }:
    /Agrob_path/agrob_pp/state { data = "PLANNING_SUCCESSFUL" }
    causes /Agrob_path/plan_pub
    within 1 s
''',

'''
# id: first_plan
# title: "First Successful Plan"
# description: "[Helper] The system produces at least one plan."
globally:
    some /Agrob_path/agrob_pp/state { data = "PLANNING_SUCCESSFUL" }
    within 300 s
''',

'''
# id: second_plan
# title: "Second Successful Plan"
# description: "[Helper] The system produces a second plan."
after /Agrob_path/agrob_pp/state { data = "PLANNING_SUCCESSFUL" }:
    some /Agrob_path/agrob_pp/state { data = "PLANNING_SUCCESSFUL" }
    within 300 s
''',
]


def test_me():
    from hpl.parser import property_parser
    p = property_parser()
    r = TemplateRenderer()
    outputs = []
    for text in AGROB_EXAMPLES:
        hpl_property = p.parse(text)
        code = r.render_monitor(hpl_property)
        outputs.append(code)
    print('\n\n'.join(code for code in outputs))


if __name__ == '__main__':
    test_me()
