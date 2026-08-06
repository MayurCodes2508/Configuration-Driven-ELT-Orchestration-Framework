from el_system.job_executors.auth.registries.strategies import AuthRegistry


class Auth:
    @classmethod
    def get_auth(cls, auth_cfg, auth_type):

        auth = AuthRegistry.get_obj(auth_cfg=auth_cfg, auth_type=auth_type)

        secret = auth.secret

        return secret
