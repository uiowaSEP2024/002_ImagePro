# Discovery notes:

* ## Setting up env files: 
  * default password = admin1234
  * For initial setup all env files should be the same
  * For production, the .env.prod file should be different
  * NOTE: Need to update default password **everywhere**
  * Im noticing that we are getting some errors: 
    * `LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
  * 96% Code coverage is impressive we need to keep it that way
  * 

* ## General
* It isn't clear but _**docs/botImage/docs/**_ has the docs you want to view first when attempting to understand the project. It is the first doc you want to understand when you are trying to understand the project.
* The API Documentation is Missing so that is a good first task. TODO - Add API Documentation
* Documentation needs to be condensed or make more linear it is kind of overwhelming
* The frontend pages api dont seem to be useful at all. `frontend/src/pages/api`
* The frontend Readme seems to be out of date. `frontend/README.md`
* Seems to be writtn in TypeScript-- Need to find out if anyone knows this better and can help with this
* Need to reaserch [FastAPI](https://fastapi.tiangolo.com/) and [SQLAlchemy](https://www.sqlalchemy.org/) 
* Need to figure out how to make admin accounts and basic user accounts or if that is already done the login info
* 