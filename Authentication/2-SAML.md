![saml auth flow](./image/saml-auth.png)

# Components of system
- User: Requests a service from the application.

- Web browser: The component that the user interacts with.

- Web app: Enterprise application that supports SAML and uses Azure AD as IdP.

- Token: A SAML assertion (also known as SAML tokens) that carries sets of claims made by the IdP about the principal (user). It contains authentication information, attributes, and authorization decision statements.

- Azure AD: Enterprise cloud IdP that provides SSO and Multi-factor authentication for SAML apps. It synchronizes, maintains, and manages identity information for users while providing authentication services to relying applications.