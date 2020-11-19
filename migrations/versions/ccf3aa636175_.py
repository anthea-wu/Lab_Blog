"""empty message

Revision ID: ccf3aa636175
Revises: 8ddf95d498f9
Create Date: 2020-11-19 10:04:41.671862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccf3aa636175'
down_revision = '8ddf95d498f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('BlogCategorys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('BlogPosts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('category', sa.Integer(), nullable=True),
    sa.Column('author', sa.Integer(), nullable=True),
    sa.Column('blog', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('edit_date', sa.DateTime(), nullable=True),
    sa.Column('slug', sa.String(length=256), nullable=True),
    sa.Column('flag', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['UserRegister.id'], ),
    sa.ForeignKeyConstraint(['blog'], ['BlogMains.id'], ),
    sa.ForeignKeyConstraint(['category'], ['BlogCategorys.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('BlogPosts')
    op.drop_table('BlogCategorys')
    # ### end Alembic commands ###
