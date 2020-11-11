"""
@author MrDrProfNo

Tool to help with the generation of JSON formatted data as expected by Joyce's
site for Operations. Format of such data follows:

    {
        "slug": "op_slug",
        "name": "op_name",
        "tier": "roman_numeral_tier",
        "type": "op_type",
        "description": "op_description",
        "energy_cost": "op_cost_energy",
        "casting": "op_cp_cost",
    },
    ...

"""

from sys import argv, stderr
from re import findall, sub, escape, IGNORECASE
from rpk_reader import rip_text_replacement


# template:
#   "[/]": "<></>",
replacement_mapping = {
    "[br/]": "<br>",
    "[Influence/]": "<influence></influence>",
    "[supply/]": "<food></food>",
    "[happiness/]": "<happiness></happiness>",
    "[operationstrength/]": "<operationstrength></operationstrength>",
    "[abilityblue]": "<actionblue>",
    "[/abilityblue]": "</actionblue>",
    "[Research/]": "<research></research>",
    "[energy/]": "<energy></energy>",
    "[operationDefense/]": "<operationDefense></operationDefense>",
    "[hp/]": "<hp></hp>",
    "[Shield/]": "<shield></shield>",
    "[turn/]": "<turn></turn>",
    "[StrengthPhysical/]": "<StrengthPhysical></StrengthPhysical>",
    "[abilityRed]": "<abilityRed>",
    "[/abilityRed]": "</abilityRed>",
    "[damagePhysical/]": "<DamagePhysical></DamagePhysical>",
    "[opinion0/]": "<raceRelation></raceRelation>",
    "[production/]": "<production></production>",
    "[firecol]": "<abilityRed>",  # this seems to be just another red text thing
    "[/firecol]": "</abilityRed>",
    "[anger/]": "<unhappiness></unhappiness>",
    "[rioter/]": "<rioter></rioter>",
    "[strengthPsyche/]": "<strengthpsyche></strengthpsyche>",
    "[damageThermal/]": "<DamageThermal></DamageThermal>",
    "[thermalDamage/]": "<DamageThermal></DamageThermal>",  # yes there are 2
    "[strengthWave/]": "<StrengthWave></StrengthWave>",  # arc status symbol
    "[damageWave/]": "<DamageWave></DamageWave>",  # arc damage symbol
    "[defenseThermal/]": "<DamageThermal></DamageThermal>",
    "[defenseBio/]": "<DamageBio></DamageBio>",
    "[population/]": "<population></population>",
    "[StrengthThermal/]": "<StrengthThermal></StrengthThermal>",
    "[casusBelli/]": "<casusBelli></casusBelli>",
    "[reputation6/]": "<reputation6></reputation6>",
    "[armor/]": "<armor></armor>",
    "[food/]": "<food></food>",
    "[strengthbio/]": "<StrengthBio></StrengthBio>",
    "[damagebio/]": "<DamageBio></DamageBio>",
    "[moveWalk/]": "<mp></mp>",
    "[damagePsyche/]": "<DamagePsyche></DamagePsyche>",
    "[defensePsyche/]": "<DamagePsyche></DamagePsyche>",
    "[resistancePsyche/]": "<DamagePsyche></DamagePsyche>",
    "[diplomaticlinks/]": "<diplolinks></diplolinks>",
    "[productioncol]": "<abilityRed>",
    "[/productioncol]": "</abilityRed>",
    "[strengthEntropy/]": "<strengthEntropy></strengthEntropy>",
    "[damageEntropy/]": "<damageEntropy></damageEntropy>",
    "[defenseEntropy/]": "<damageEntropy></damageEntropy>",
    "[essencecharge/]": "<essenceCharge></essenceCharge>",
    "[essenceAll/]": "<essenceAll></essenceAll>",
    "[foodslot/]": "<foodslot></foodslot>",
    "[researchslot/]": "<researchslot></researchslot>",
    "[energyslot/]": "<energyslot></energyslot>",
    "[productionSlot/]": "<productionSlot></productionSlot>",
    "[watersector/]": "<watersector></watersector>",
    "[tricorium/]": "<tricorium></tricorium>",
    "[medalgold/]": "<x-medal_prime></x-medal_prime>",
    "[medaliron/]": "<x-medal_veteran></x-medal_veteran>",
    "[bulletlist]": "",
    "[/bulletlist]": "",
    "[bullet]": "<bullet>",
    "[/bullet]": "</bullet>",
    "[darkgrey]": "",
    "[/darkgrey]": "",
    "[accuracy/]": "<accuracy></accuracy>"
}

tier_numerals = {
    "1": "I",
    "2": "II",
    "3": "III",
    "4": "IV",
    "5": "V",
    "6": "VI",
    "7": "VII",
    "8": "VIII",
    "9": "IX",
    "10": "X",
    "11": "XI"
}


def replace_text(replacement_dict: dict, string):
    """
    Handles text replacement on any of the strings that are known.

    :param replacement_dict: dictionary mapping replacement markers to
    replacement text.
    :param string: string to run replacement on
    :return: string with elements replaced.
    """

    # regex searches for all curly braces with content in the middle
    results = findall(r"\{.*?\}", string)

    for key in results:
        values = replacement_dict.get(key)

        # key doesn't exist
        if not values:
            continue
        # Only one value given; autoreplace it
        elif len(values) == 1:
            string = string.replace(key, values[0])
        # more than one value given, let user decide
        else:
            print("Select from options for: " + key)

            for value_pos in range(0, len(values)):
                print("    " + str(value_pos) + ". " + values[value_pos])
            while True:
                selection = input("Selection: ")

                try:
                    selection = int(selection)
                    string = string.replace(key, values[selection])
                    break
                except ValueError:
                    print("Unrecognized selection: " + str(selection))
                except IndexError:
                    print("Unrecognized selection: " + str(selection))
    return string


def replace_icon_formatting(string):
    """
    Replaces the codes for in-game icons with the ones from Joyce's site.
    :param string: String to run replacement on.
    :return:
    """

    for key in replacement_mapping.keys():
        # escapes the key for use as a regex; otherwise, the brackets cause
        # problems.
        regex_key = escape(key)

        # replaces all instances of the key (in-game icon representation) with
        # the associated value (css style formatting for the same icon),
        # ignoring case.
        string = sub(regex_key, replacement_mapping[key], string, flags=IGNORECASE)

    # regex matches any brackets that remain; there shouldn't be any
    missed_list = findall(r"\[.*?\]", string)
    for missed_icon in missed_list:
        print("ERROR: Unrecognized icon tag: " + missed_icon, file=stderr)

    return string


def main():
    if len(argv) != 2:
        print("usage: op_description_helper <output_file>")
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

        tier_number = input("Enter tier number (numeric): ")

        if not tier_number in tier_numerals.keys():
            print("invalid tier number")
            continue

        tier_numeral = tier_numerals[tier_number]
        while True:
            print("Enter the type of the operation (some operations "
                  "will ask for subtypes): \n"
                  "    1. Tactical Operation\n"
                  "    2. Strategic Operation\n"
                  "    3. Covert Operation\n"
                  "    4. Doctrine Operation\n"
                  "    5. Empire Upgrade")

            op_type = input()

            # tac ops
            if op_type == "1":

                # flag used to identify which cost icon to use later
                op_is_tactical = True
                print("Enter subtype of: Tactical Operation\n"
                      "    1. Instant\n"
                      "    2. Battlefield\n"
                      "    3. Summon")
                op_subtype = input()

                if op_subtype == "1":
                    op_type_string = "Tactical Operation (Instant)"
                elif op_subtype == "2":
                    op_type_string = "Tactical Operation (Battlefield)"
                elif op_subtype == "3":
                    op_type_string = "Tactical Operation (Summon)"

            # strat ops
            elif op_type == "2":

                # flag used to identify which cost icon to use later
                op_is_tactical = False
                print("Enter subtype of: Strategic Operation\n"
                      "    1. Instant\n"
                      "    2. Timed\n"
                      "    3. Sustained\n"
                      "    4. Summon\n"
                      "    5. Doomsday Finisher")

                op_subtype = input()

                if op_subtype == "1":
                    op_type_string = "Strategic Operation(Instant)"
                elif op_subtype == "2":
                    op_type_string = "Strategic Operation (Timed)"
                elif op_subtype == "3":
                    op_type_string = "Strategic Operation (Sustained)"
                elif op_subtype == "4":
                    op_type_string = "Strategic Operation (Summon)"
                elif op_subtype == "5":
                    op_type_string = "Doomsday Finisher Operation"

            # covert ops
            elif op_type == "3":
                op_is_tactical = False
                op_type_string = "Covert Operation"

            # doctrines
            elif op_type == "4":
                op_is_tactical = False
                op_type_string = "Doctrine Operation"

            # empire upgrades
            elif op_type == "5":
                op_is_tactical = False
                print("Enter subtype of: Empire Upgrade\n"
                      "    1. Colony Upgrade\n"
                      "    2. Empire Upgrade\n"
                      "    3. Sector Upgrade")

                op_subtype = input()

                if op_subtype == "1":
                    op_type_string = "Colony Upgrade"
                elif op_subtype == "2":
                    op_type_string = "Empire Upgrade"
                elif op_subtype == "3":
                    op_type_string = "Sector Upgrade"

            # invalid option chosen
            else:
                print("unrecognized op type")
                continue

            break

        original_description = input("Copy-paste Description below:\n")

        text_replaced_description = replace_text(replacement_dict, original_description)

        print("Any variables which were not automatically replaced will appear "
              "below; fill in the correct value, including relevant symbol if "
              "none is present.")

        # regex searches for all curly braces with content in the middle
        variable_slots = findall(r"\{.*?\}", text_replaced_description)

        for variable in variable_slots:
            replacement = input(variable + " = ")
            text_replaced_description = text_replaced_description.replace(variable,
                                                                  replacement)

        icon_replaced_description = replace_icon_formatting(text_replaced_description)

        print("Description now reads: \n" + icon_replaced_description)

        op_energy_cost = input("Operation energy cost: ")
        op_point_cost = input("Operation casting point cost: ")

        if op_is_tactical:
            casting_point_icon = "<tacticalPoint></tacticalPoint>"
        else:
            casting_point_icon = "<stratPoint></stratPoint>"

        output_file.write(
            """
        {
            "slug": \"""" + op_slug + """\",
            "name": \"""" + op_name + """\",
            "tier": \"""" + tier_numeral + """\",
            "type": \"""" + op_type_string + """\",
            "description": \"""" + icon_replaced_description + """\",
            "energy_cost": \"""" + op_energy_cost + """\",
            "casting": \"""" + op_point_cost + """ """ + casting_point_icon + """\",
        },
            """
        )

        output_file.flush()


if __name__ == '__main__':
    main()
