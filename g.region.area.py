#!/usr/bin/env python3
#
############################################################################
#
# MODULE:      g.region.area
# AUTHOR(S):   Anika Weinmann
#
# PURPOSE:     Computes the area in sqm and compares it with the maximum
# COPYRIGHT:   (C) 2020-2022 by mundialis GmbH & Co. KG and the GRASS Development Team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
#############################################################################
# %module
# % description: Computes the current region extent or the size of the map in square meters and compares it with the user defined maximum.
# % keyword: general
# % keyword: area
# % keyword: vector
# %end

# %option G_OPT_V_INPUT
# % key: map
# % required: no
# % description: Input vector map to compute the area, if not set the current region is used
# %end

# %option
# % key: maximum
# % type: double
# % required: no
# % multiple: no
# % label: Maximum area in sqm for comparison
# %end

# %flag
# % key: t
# % description: Do not throw error, if region area is greater than the maximum
# %end

import atexit
import os
import random
import string

import grass.script as grass

# initialize global vars
rm_vectors = []


def cleanup():
    grass.message(_("Cleaning up..."))
    nuldev = open(os.devnull, "w")
    for rm_v in rm_vectors:
        grass.run_command(
            "g.remove", flags="f", type="vector", name=rm_v, quiet=True, stderr=nuldev
        )


def main():

    global rm_vectors

    # test overlap
    grass.message("Create vector map out of current region ...")
    tmpvector = "tmp_regionvector_%s" % "".join(
        random.choice(string.ascii_letters) for i in range(5)
    )
    rm_vectors.append(tmpvector)
    if not options["map"]:
        grass.run_command("v.in.region", output=tmpvector, quiet=True)
    else:
        grass.run_command("g.copy", vector="%s,%s" % (options["map"], tmpvector))

    grass.message("Computing area of current region in sqm ...")
    if len(grass.vector_db(tmpvector)) == 0:
        grass.run_command("v.db.addtable", map=tmpvector, quiet=True)
    grass.run_command(
        "v.db.addcolumn",
        map=tmpvector,
        columns="tmparea double precision",
        quiet=True,
        overwrite=True,
    )
    grass.run_command(
        "v.to.db",
        map=tmpvector,
        option="area",
        columns="tmparea",
        units="meters",
        quiet=True,
        overwrite=True,
    )

    grass.message("Select area ...")
    area_sqm = float(
        [
            x
            for x in grass.parse_command(
                "v.db.select", map=tmpvector, columns="tmparea", flags="c"
            )
        ][0]
    )
    grass.message(_("The region has an area of %.2f sqm") % area_sqm)

    if options["maximum"]:
        maximum = float(options["maximum"])
        if maximum < area_sqm:
            msgfn = grass.fatal
            if flags["t"]:
                msgfn = grass.warning
            msgfn(
                _(
                    "The region has with %.2f sqm a larger area than the "
                    "given maximum (%.2f sqm)"
                    % (area_sqm, maximum)
                )
            )
        else:
            grass.message(
                _(
                    "The region has with %.2f sqm a smaller area than the "
                    "given maximum (%.2f sqm)"
                    % (area_sqm, maximum)
                )
            )


if __name__ == "__main__":
    options, flags = grass.parser()
    atexit.register(cleanup)
    main()
