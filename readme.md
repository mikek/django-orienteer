#Orienteer

Orienteer is simple Compass integration for Django projects. It is the easiest
way to give Compass/Sass projects first class status inside your Django
project.

Once you define the settings below and add template tags to your template, fire
up the development server. If a CSS file seems to be out-of-date and
**TEMPLATE_DEBUG is True**, Orienteer will run Compass to generate your CSS for
you. Be sure to *carefully read the instructions* below for settings specifics.

##Usage

###Required settings

In your Django settings.py file, define the path to compass project root.

    COMPASS_PROJECT_DIR = STATIC_ROOT + 'css/'

Then, define the css output directory. **This is relative to the project
directory.**

    COMPASS_OUTPUT_DIR = './'

Also, set the URL where your output files will be accessed.

    COMPASS_OUTPUT_URL = STATIC_URL + 'css/'

Finally, define where the compass binary is (it can be relative if binary is
in the *PATH* environment variable).

    COMPASS_BIN = '/usr/bin/compass'

###Optional settings

Set path to the compass/scss files. Default is 'src'.

    COMPASS_SOURCE_DIR = 'sass'

Provide any other options to the comapass.

    COMPASS_EXTRA_OPTS = '--time --boring'

Turn off timestamps in generated css path if you want for some reason.

    COMPASS_USE_TIMESTAMP = False

Show exact compass command used on *sdterr*. It is equal to `DEBUG`
by default.

    COMPASS_DEBUG = True

You can also use standard compass configuration file *config.rb* in the
`COMPASS_PROJECT_DIR` directory.

###Templates

Next, in your template file you can reference your Sass file along with which
media type(s) it is and the appropriate style tag will be generated.

    {% load orienteer %}
    {% compass 'my_style' 'screen' %}

This will check your Compass project's `COMPASS_SOURCE_DIR` directory for the
'my_style.sass' file, compile it if necessary, and then output the following
HTML tag:

    <link href='/media/css/my_style.css?1273972058.0' rel='stylesheet' type='text/css' media='screen'/>

That's it!

##Documentation

View [Sass documentation](http://sass-lang.com/docs.html) and
[Compass documentation](http://compass-style.org/reference/compass/) for
details on syntax.

Also, be sure to visit the
[Compass Google Group](http://groups.google.com/group/compass-users)
for help with Compass related issues.


##Requirements

- [Python](http://python.org/) (2.5 or greater, but not 3.x)
- [Django](http://www.djangoproject.com/) (1.0 or greater)
- Obviously you'll nedd to have [Compass](http://compass-style.org) installed
on your developmnet machine.

##Acknowledgements

Special thanks to Ash Christopher (ash@newthink.net) for providing the clever
Django Sass app which was the inspiration for this one.
