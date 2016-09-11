# Project 2: Building a Portfolio Website

Create a responsive portfolio web site.

## Disclaimer

The **ZOOR** and **HYPERTRADE** projects are, either partially or wholly,
fictions of my imagination, but I've included them to add some meat to the
portofolio, otherwise I would have had very little to play with. **HYPERTRADE**
is completely made up. **ZOOR**, on the other hand, is an actual project of mine
that I've been working on for some months, but it is far from being production
ready.

## Optimized website

To generate the optimized version of the website, you can run `grunt`, which
will generate a directory named *production*, which mirrors *proj2*, and
contains the following optimizations:

* minimized HTML
* minimized CSS
* smaller and compressed pictures

In addition to optimizing the website, running `grunt` validates the
correctness of the HTML and CSS, and any errors found are reported. If there is
a desire to validate the HTML and CSS without optimizing the website, then it
can be achieved by running `grunt valid` to validate the HTML, and `grunt css`
to validate the CSS.

To learn more about **GRUNT**, see their [getting started][1] guide.

[1] http://gruntjs.com/getting-started
