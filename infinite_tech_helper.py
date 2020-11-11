from sys import argv
from op_description_helper import rip_text_replacement, tier_numerals, \
    replace_text, findall, replace_icon_formatting


def main():
    if len(argv) != 2:
        print("usage: infinite_tech_helper <output_file>")
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

        op_name = input("Enter operation name (enter nothing to stop): ")

        if op_name == "":
            print("exiting...")
            return 0

        op_slug = op_name.lower().replace(" ", "_")

        tier_number = "11"

        tier_numeral = tier_numerals[tier_number]
        op_type_string = "Empire Upgrade"

        description = ""
        print("BEGIN entering the title/description pairs")

        while True:
            name = input("Unlock name (press Enter to finish): ")
            if name == "":
                break

            name = "<titlebrown>" + name + "</titlebrown>"

            description += name + "<br>"

            unlock_description = input("Unlock description: \n")

            description += unlock_description + "<br>"

        print("Any variables which were not automatically replaced will appear "
              "below; fill in the correct value, including relevant symbol if "
              "none is present.")
        text_replaced_description = replace_text(replacement_dict, description)

        # regex searches for all curly braces with content in the middle
        variable_slots = findall(r"\{.*?\}", text_replaced_description)

        for variable in variable_slots:
            replacement = input(variable + " = ")
            text_replaced_description = text_replaced_description.replace(variable,
                                                                  replacement)

        icon_replaced_description = replace_icon_formatting(text_replaced_description)

        print("Description now reads: \n" + icon_replaced_description)

        output_file.write(
            """
        {
            "slug": \"""" + op_slug + """\",
            "name": \"""" + op_name + """\",
            "tier": \"""" + tier_numeral + """\",
            "type": \"""" + op_type_string + """\",
            "description": \"""" + icon_replaced_description + """\",
        },
            """
        )

        output_file.flush()


if __name__ == '__main__':
    main()
