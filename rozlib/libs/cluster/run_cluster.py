# config
# load: src -> tgt paths (for copying to machine) (make sure dirs exist)
# post-load: e.g. list of things to unzip

# post-run (e.g. zip)
# write-back src -> tgt path

# todo(low): questions
# - should models be placed in other places?

# todo misc
# - activate conda in command
# - git pull / sync conda / pip

# def setup_on_machine():
#     # todo: log what machine we're on
#
#     copy_files_to_machine()
#
#     # todo: unzip / prep any files
#     # any checks that the process worked
#
#     # todo: run actual code (wrap try catch)
#
#     # note that these two things could be done by another job but prob okay
#     # todo: post run (eg zip)
#     # todo: copy back
#
#
# def copy_files_to_machine():
#     # get scratch dirs (see nlp doc)
#
#     # copy files (see load above in config)
