import commands, sys
import platform


def get_base_url_from_config():
    try:
        from resource_management.libraries.script.script import Script
        from resource_management.libraries.functions.default import default
        from resource_management.core.logger import Logger

        config = Script.get_config()
        repositories = config['repositoryFile']['repositories']
        stack_name = default("/clusterLevelParams/stack_name", None)
        stack_name_uppercase = stack_name.upper()
        baseurl = None

        Logger.info("repositories: {0}".format(repositories))
        for repo in repositories:
            if repo['repoName'] == stack_name_uppercase:
                baseurl = repo['baseUrl']
                Logger.info("baseUrl: {0}".format(baseurl))
        return baseurl
    except Exception:
        return None


def get_colon_separated_value(s):
    start_pos = s.find(":") + 1
    return s[start_pos:].strip()


def get_base_url_from_yum():
    package_name = "zookeeper"
    repo_line = commands.getoutput("yum --disablerepo '*' --enablerepo  'HD*' info {} 2>/dev/null | grep 'Repo'".format(package_name))
    if 'ppc' in platform.processor():
        repo_line = commands.getoutput("yum --disablerepo '*' --enablerepo  'HD*' info {} 2>/dev/null | grep 'repo'".format(package_name))
    repo_name = get_colon_separated_value(repo_line)
    if repo_name == "":
        print("ERROR: Cannot find repo for {}".format(package_name))
        sys.exit(-1)

    print("Repo name: {}".format(repo_name))

    baseurl_line = commands.getoutput("yum repolist {} -v | grep baseurl".format(repo_name))
    baseurl = get_colon_separated_value(baseurl_line)
    print("Base URL: {}".format(baseurl))
    return baseurl


baseurl = get_base_url_from_config()

if baseurl is None:
    baseurl = get_base_url_from_yum()
