class DependencyResolver:

    def resolve(self, metadata):

        dependencies = metadata.get("dependencies", [])

        resolved = []

        for dep in dependencies:

            resolved.append(dep)

        return resolved
