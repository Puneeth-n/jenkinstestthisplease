# Jenkinstestthisplease

# What is this?
Since we moved to [Jenkins Blue ocean](https://jenkins.io/projects/blueocean/) and [GitHub Branch Source plugin](https://wiki.jenkins.io/display/JENKINS/GitHub+Branch+Source+Plugin) from [ghprb](https://github.com/janinko/ghprb), we started missing the functionality of triggering Jenkins builds from GitHub comments. Call it **commentOps**

We were used to commenting `Test this please` on `PR`s to trigger tests on Jenkins.

So this small service brings back the good Ol functionality.

# Ok cool! How do I install it?
well, there is a docker image at `puneethn/jenkinstestthisplease:latest` You could start off by downloading this repo and running `make start`.

However, there are somethings you might want to have for it to work.

1. Get hold of your `JENKINS_USERNAME`, `JENKINS_PASSWORD` and `JENKINS_URL`
2. Determine your `JENKINS_ORG`. This can be the name of your organization. ex: `jenkinsci`
3. Determine your `JENKINS_PROJECT`. This can be the name of your project. ex: `jenkins`
4. Determine your `JENKINS_BUILD_PARAMS` (if any). This can be something like `foo=bar&lorem=ipsum&...`
5. Generate a **strong** `GITHUB_S2S_SECRET` for your webhook so that [GitHub signs](https://developer.github.com/webhooks/securing/) each event with it.
6. Setup the [GitHub webhook](https://developer.github.com/webhooks/creating/)
7. Set all the `CAPITALIZED` variables as environment variables (You can also refer to the `docker-compose.yml`) and Deploy to the address setup in the webhook.
8. Comment on your `PR` something like *"Baby test this please"*, *"Darling test this please"*, *"Jenkins, test this please"* and see your PR's being built.


# TODO:
- Support multiple projects
- Support whielisting and Blacklisting Users 
   
