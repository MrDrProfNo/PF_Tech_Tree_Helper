"""
@author MrDrProfNo

Testing that commits still work?

Tool to help with generation of building descriptions. Buildings are formatted
much like operations, but use some different bits of information and have a
different "copy-paste flow."
"""

from sys import argv
from op_description_helper import rip_text_replacement, replace_icon_formatting, replace_text, tier_numerals, replacement_mapping
from re import findall


def replace_remaining_variables(text_replaced_description):

    # regex searches for all curly braces with content in the middle
    variable_slots = findall(r"\{.*?\}", text_replaced_description)

    for variable in variable_slots:
        replacement = input(variable + " = ")
        text_replaced_description = text_replaced_description.replace(
            variable,
            replacement)

    return text_replaced_description

def main():
    if len(argv) != 2:
        print("usage: tech_contents_helper <output_file>")
        return -1

    output_file = open(argv[1], "a+")

    rpk_filename = input("If you want to load text replacement from an RPK, "
                         "enter its absolute filepath below:\n")

    if rpk_filename != "":
        replacement_dict = rip_text_replacement(rpk_filename)
    else:
        replacement_dict = {}

    while True:
        print("#" * 30)

        op_name = input("Enter building name (enter nothing to stop): ")

        if op_name == "":
            print("exiting...")
            return 0

        op_slug = op_name.lower().replace(" ", "_")

        tier_number = input("Enter tier number (numeric): ")

        if not tier_number in [str(i) for i in range(0, 11)]:  # generates array of str(valid tier numbers)
            print("invalid tier number")
            continue

        tier_numeral = tier_numerals[tier_number]

        while True:
            print("Enter Building Type:\n"
                  "    1. Sector Upgrade\n"
                  "    2. Colony Upgrade\n")

            building_type = input()

            if building_type not in ["1", "2"]:
                print("unrecognized building type: " + building_type)
                continue

            if building_type == "1":
                type_string = "Sector Upgrade"
            else:
                type_string = "Colony Upgrade"
            break

        original_description = input("Copy-paste Description below:\n")

        text_replaced_description = replace_text(replacement_dict,
                                                 original_description)

        print("Any variables which were not automatically replaced will appear "
              "below; fill in the correct value, including relevant symbol if "
              "none is present.")

        text_replaced_description = replace_remaining_variables(text_replaced_description)

        while True:
            level_number_choice = input(
                "Does this building have any Levels in its description?\n"
                "    1. 0 tiers (most buildings)\n"
                "    2. 3 tiers (Water sectors, doomsdays)\n"
                "    3. 5 tiers (other sectors)\n"
            )

            if level_number_choice not in ["1", "2", "3"]:
                print("invalid tier choice: " + level_number_choice)
                continue
            else:
                break

        if level_number_choice == "1":
            level_max = 0
        elif level_number_choice == "2":
            text_replaced_description += "<br><br>"
            level_max = 3
        elif level_number_choice == "3":
            text_replaced_description += "<br><br>"
            level_max = 5
        for level in range(0, level_max):
            print("Copy-paste level " + str(level + 1) +
                  " description below:")

            # get the description
            level_description = input()

            # run text replacement for variables
            level_text_replaced_description = replace_text(
                replacement_dict, level_description
            )

            level_text_replaced_description = replace_remaining_variables(
                level_text_replaced_description
            )

            # add the level to the description
            text_replaced_description += (
                    "<bullet> Level " + str(level + 1) + "<br>"
                    + level_text_replaced_description
                    + "</bullet>"
            )

        icon_replaced_description = replace_icon_formatting(
            text_replaced_description)

        print("Description now reads: \n" + icon_replaced_description)

        prod_cost = input("Building Production Cost: ")
        energy_cost = input("Building Energy Cost: ")
        cosmite_cost = input("Building Cosmite Cost: ")
        upkeep_cost = input("Building Upkeep Cost: ")

        ignore_strings = ["", "0"]

        output_file.write(
"""
        {
            "slug": \"""" + op_slug + """\",
            "name": \"""" + op_name + """\",
            "tier": \"""" + tier_numeral + """\",
            "type": \"""" + type_string + """\",
            "description": \"""" + icon_replaced_description + """\",
            "production_cost": \"""" + prod_cost + """ <production></production> Production",
            """ + ("\"energy_cost\": \"" + energy_cost + " <energy></energy> Energy\"," if not energy_cost in ignore_strings else "") + """
            """ + ("\"cosmite_cost\": \"" + cosmite_cost + " <tricorium></tricorium> Cosmite\"," if not cosmite_cost in ignore_strings else "") + """
            """ + ("\"upkeep_cost\": \"" + upkeep_cost + " <energy></energy> / <turn></turn>\"," if not upkeep_cost in ignore_strings else "") + """
        },
"""
        )

        output_file.flush()


if __name__ == '__main__':
    main()
