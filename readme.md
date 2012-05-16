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

In your Django settings.py file, define **absolute path** to compass project
root.

    COMPASS_PROJECT_DIR = YOUR_PROJECT_ROOT + 'css/'

Also, set the URL where your output files will be accessed. Can be ommited if
`STATIC_URL` is set.

    COMPASS_OUTPUT_URL = "%scss" % STATIC_URL

###Optional settings

Define the css output directory. **This is relative to the compass project
directory** and defaults to it.

    COMPASS_OUTPUT_DIR = './'

Path to the compass script and ruby binary (can be just a name if *PATH*
environment variable is set appropriately). Default script name is 'compass'.
Default ruby binary is an empty string, and the script will be executed
directly.

    COMPASS_SCRIPT = '/usr/bin/compass'
    COMPASS_RUBY_BIN '/usr/bin/ruby'

(On Windows, however, you should specify full paths in the following
format: "C:\\Ruby193\\bin\\ruby.exe")

Set compass project relative path to the compass/scss files. Default is 'src'.

    COMPASS_SOURCE_DIR = 'sass'

Provide any other options to the comapass.

    COMPASS_EXTRA_OPTS = '--time --boring'

Turn off timestamps in generated css path if you want for some reason.

    COMPASS_USE_TIMESTAMP = False

Bypass compass if newest source and target file timestamps are equal. (This
might happen in some rare cases, maybe caused by some stupid VCS or compass
frontends.)

    COMPASS_SKIP_ON_EQUAL_TIMESTAMP = True

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
