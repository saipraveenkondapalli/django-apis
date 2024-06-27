# API for portfolio websites

[![Testing Status](https://github.com/saipraveenkondapalli/django-apis/actions/workflows/django.yml/badge.svg)](https://github.com/saipraveenkondapalli/django-apis/actions/workflows/django.yml/badge.svg)

## Endpoints

>[!IMPORTANT]
> To make an api request to the backend, we need to verify the site requesting the resource. You need to provide site id with every request in the header or in the URL params
> The backend verifies the request with origin site and matches with the site id. 

```
URL: https://<url>/<resource>/?site=<site_id>
Header: X-SITE-ID: <site_id>
```



| Endpoint                      | Description                                            | Method | Request Body         | Response Body                                    |
|-------------------------------|--------------------------------------------------------|--------|----------------------|--------------------------------------------------|
| /api/contact/                 | To store a contact form data                           | POST   | name, email, message | {"status": "success"}                            |
| /api/resume/                  | redirects to resume url                                | GET    |                      |                                                  | 
| /api/job-application-message/ | display a custom message to the visitor of the website | GET    |                      | {"message": "Thank you for visiting my website"} |

