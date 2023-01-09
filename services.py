import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import email_validator as _email_check
import passlib.hash as _hash
import jwt as _jwt
import database as _database
import models as _models
import schemas as _schemas

_JWT_SECRET = "donotthinkaboutit"
oath2schema = _security.OAuth2PasswordBearer("/api/token")


def get_select(user, db, post):
    try:
        result = db.query(_models.Post).filter_by(id=post.id, owner_id=user.id).one()
    except:
        raise _fastapi.HTTPException(status_code=404, detail="Post not found")
    return result


def _create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()


async def create_user(user: _schemas.UserCreate, db: _orm.Session):
    # check that email is valid
    try:
        valid = _email_check.validate_email(email=user.email)
        email = valid.email
    except _email_check.EmailNotValidError:
        raise _fastapi.HTTPException(
            status_code=404, detail="Please enter a valid email"
        )
    hashed_password = _hash.bcrypt.hash(user.password)
    user_obj = _models.User(email=email, hashed_password=hashed_password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def create_token(user: _models.User):
    user_schema_obj = _schemas.User.from_orm(user)
    user_dict = user_schema_obj.dict()
    del user_dict["date_created"]
    token = _jwt.encode(user_dict, _JWT_SECRET)
    return dict(access_token=token, token_type="bearer")


async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(email=email, db=db)
    if not user:
        return False
    if not user.verify_password(password=password):
        return False
    return user


async def get_current_user(
    db: _orm.Session = _fastapi.Depends(get_db),
    token: str = _fastapi.Depends(oath2schema),
):
    try:
        payload = _jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid email or password"
        )
    return _schemas.User.from_orm(user)


async def create_post(user: _schemas.User, db: _orm.Session, post: _schemas.PostCreate):
    post = _models.Post(**post.dict(), owner_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return _schemas.Post.from_orm(post)


async def view_user_posts(user: _schemas.User, db: _orm.Session):
    posts = db.query(_models.Post).filter_by(owner_id=user.id)
    return list(map(_schemas.Post.from_orm, posts))


async def delete_post(user: _schemas.User, db: _orm.Session, post: _schemas.PostDelete):
    delete = get_select(user, db, post)
    db.delete(delete)
    db.commit()
    return _schemas.PostDelete.from_orm(post)


async def update_post(user: _schemas.User, db: _orm.Session, post: _schemas.PostUpdate):
    update = get_select(user, db, post)
    update.post_text = post.post_text
    db.add(update)
    db.commit()
    db.refresh(update)
    return _schemas.PostUpdate.from_orm(post)


async def update_like(
    user: _schemas.User, db: _orm.Session, post: _schemas.PostLikeUpdate
):
    try:
        post_select = db.query(_models.Post).filter_by(id=post.id).one()
    except:
        raise _fastapi.HTTPException(status_code=404, detail="Post not found")
    if user.id != post_select.owner_id:
        if post.like > 0:
            post_select.likes += 1
            _schemas.In_memory.posts[post.id]["likes"] += 1
        elif post.like < 0:
            post_select.dislikes += 1
            _schemas.In_memory.posts[post.id]["dislikes"] += 1
        else:
            raise _fastapi.HTTPException(
                status_code=400, detail="'like' must be greater than or less than zero"
            )
        db.add(post_select)
        db.commit()
        db.refresh(post_select)
    else:
        raise _fastapi.HTTPException(
            status_code=400, detail="You won't be able to like your own posts"
        )
    return _schemas.PostLikeUpdate.from_orm(post)

