"""Provides an extension to allow front matter in the template"""
from jinja2 import Environment
from jinja2.ext import Extension

from ..defaults import FRONT_MATTER_LANG


class FrontMatterExtension(Extension):
    """This extension allows to have front matter"""

    def __init__(self, environment: Environment) -> None:
        super().__init__(environment)
        environment.extend(front_matter_lang=FRONT_MATTER_LANG)

    def preprocess(self, source: str, name: str, filename: str = None) -> str:
        import frontmatter

        if self.environment.front_matter_lang.lower() == "toml":
            from frontmatter.default_handlers import TOMLHandler as handler
        elif self.environment.front_matter_lang.lower() == "json":
            from frontmatter.default_handlers import JSONHandler as handler
        else:
            from frontmatter.default_handlers import YAMLHandler as handler

        processed = frontmatter.loads(source, handler=handler())
        self.environment.globals["page"] = processed
        return processed.content
