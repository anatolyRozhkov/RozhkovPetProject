from pytest import fixture
from config import Config

"""
FIXTURES
"""


@fixture(scope="session")
def drv(app_config, get_parameters):
    """
    app_config.browser returns a list
    chrome, firefox, and headless keywords return a list with two items:
    webdriver object and options
    remote keyword returns a list with webdriver,
    selenium server url, and options
    """
    browser = app_config.browser[0]  # webdriver object

    if get_parameters["browser"] == "remote":
        exe_path = app_config.browser[1]  # remote server url
        ARGS = app_config.browser[2]  # options
        drv = browser(command_executor=exe_path,
                      options=ARGS)
    else:
        ARGS = app_config.browser[1]  # options
        SERVICE = app_config.browser[2]  # webdriver_manager
        drv = browser(options=ARGS, service=SERVICE)  # options

    yield drv

    drv.quit()


"""
ADD PARAMETERS
"""


def pytest_addoption(parser):
    """avoid adding on letter options like -g"""
    parser.addoption("--env",
                     action="store",
                     default="dev",
                     help="Specify environment")
    parser.addoption("--browser",
                     action="store",
                     default="chrome",
                     help="Select browser")


@fixture(scope="session")
def get_parameters(request):
    """
    detects what keywords was used with an option.
    Ex: --env prod
    """
    config_param = {
        "env": request.config.getoption("--env"),
        "browser": request.config.getoption("--browser")
    }
    return config_param


@fixture(scope="session")
def app_config(get_parameters):
    """
    Returns value from a Config dictionary
    """
    configuration = Config(get_parameters)
    return configuration
