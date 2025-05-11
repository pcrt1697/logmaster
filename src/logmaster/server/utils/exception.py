class ResourceNotFoundException(ValueError):

    @classmethod
    def by_id(cls, resource_class: type, identifier):
        return cls(
            f"{resource_class.__name__.capitalize()} with id [{identifier}] does not exists"
        )