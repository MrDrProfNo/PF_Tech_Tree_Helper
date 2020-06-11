"""

@author MrDrProfNo


Tool to help with the generation of JSON formatted data as expected by Joyce's
site for Techs. Format of such data follows:

var jsonTech = {
    "tech": [
        {
            "slug": "tech_slug",
            "name": "tech_name",

            "mod_unlock": [
                {
                    "slug": <values>
                },
                ...
            ],
            "op_unlock": [
                {
                    "slug": <values>
                },
                ...
            ],
            "unit_unlock": [
                {
                    "slug": <values>
                },
                ...
            ],
            "cost": "cost",

        },
        ...
    ]
}

Any field occupied by <values> contains a string reference derived from the name
of the element in that position: all lowercase, underscores replacing spaces,
no other replacements.

Output is appended directly to a file specified in the command line.

"""
from sys import argv
from re import search


def generate_unlock_JSON(unlock_list: list, race_name=""):
    """
    Given a list of unlocks that belong in one of the 3 categories,
    creates the string that goes in the resulting JSON file, of form:

    {
        "slug": "element1"
    },
    {
        "slug": "element2"
    },
    ...

    :param unlock_list: List of unlock names to be put into the format
    :return:
    """

    # special case for no elements
    if len(unlock_list) == 0:
        ret = \
        """
                {
                
                }
        """
        return ret

    ret = ""
    for unlock in unlock_list:
        unlock_slug = ""

        if race_name != "":
            unlock_slug += race_name.lower() + "_"

        unlock_slug += unlock + ""

        # build this element's little encasement. The indentation used here is
        # translated into the output file.
        ret += \
        """
                {
                    \"slug\": \"""" + unlock_slug + """\"
                }
        """

        # If this isn't the last element, add the comma
        if unlock_list.index(unlock) != len(unlock_list) - 1:
            ret += ","

    return ret

def main():

    if len(argv) != 2:
        print("usage: tech_contents_helper <output_file>")
        return -1

    output_file = open(argv[1], "a+")

    print("Enter tree being used (lowercase of tree name is prepended to techs)")
    race = input()

    tech_slug_prepend = race.lower()

    print("Is this a Secret Tech? Changes some internal naming schemes (y/n)")

    # If this is a secret tech, "race name" doesn't get prepended to unit
    # unlocks; instead, "secret" does
    unit_name_prepend = "secret" if input().lower() == "y" else race

    # begin the loop through input stages.
    while True:
        tech_name = input("Enter Tech Name (leave blank to quit): ")
        if tech_name == "":
            break

        tech_slug = tech_slug_prepend + "_" + tech_name.lower().replace(" ", "_")

        tech_mods = []
        tech_ops = []
        tech_units = []

        # have user enter data about the various unlocks from the tech
        while True:
            print(
                "Enter number for type of next unlock:\n"
                "   1. mod\n"
                "   2. operation\n"
                "   3. unit\n"
                "   4. No Further Input (moves to next tech)")

            unlock_type = input()

            if unlock_type == "4":
                break
            elif not len(unlock_type) == 1 and search('[1-4]', unlock_type):
                print("unrecognized type: " + unlock_type)
                continue

            unlock_name = input("Enter unlock name: \n")
            unlock_slug = unlock_name.lower().replace(" ", "_")

            if unlock_type == "1":
                tech_mods.append(unlock_slug)
            elif unlock_type == "2":
                tech_ops.append(unlock_slug)
            elif unlock_type == "3":

                if unit_name_prepend == "secret":
                    print("Should this unit have secret_ prepended (y/n)")
                    unit_name_prepend = unit_name_prepend if input().lower() == "y" else ""
                tech_units.append(unlock_slug)
            elif unlock_type == "4":
                break

        tech_cost = input("Enter tech cost: ")
        print("#" * 60)

        output_file.write(
"""
        {
            \"slug\": \"""" + tech_slug + """\",
            \"name\": \"""" + tech_name + """\",
            
            \"mod_unlock\": [ """ + generate_unlock_JSON(tech_mods) + """\n            ],
            \"op_unlock\": [""" + generate_unlock_JSON(tech_ops) + """\n            ],
            \"unit_unlock\": [""" + generate_unlock_JSON(tech_units, unit_name_prepend) + """\n            ],
            \"cost\": \"""" + tech_cost + """\",
        },
"""
        )

        output_file.flush()

    print("exiting...")


if __name__ == '__main__':
    main()
