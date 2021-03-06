"""扩充课程表，增加章节数

Revision ID: f514b4d8015f
Revises: 97c193f44a94
Create Date: 2020-09-12 14:48:55.931028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f514b4d8015f'
down_revision = '97c193f44a94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chapter',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('video_url', sa.String(length=256), nullable=True),
    sa.Column('video_duration', sa.String(length=24), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chapter_name'), 'chapter', ['name'], unique=True)
    op.add_column('course', sa.Column('image_url', sa.String(length=256), nullable=True))
    op.drop_constraint('course_ibfk_1', 'course', type_='foreignkey')
    op.create_foreign_key(None, 'course', 'user', ['author_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.create_foreign_key('course_ibfk_1', 'course', 'user', ['author_id'], ['id'], ondelete='CASCADE')
    op.drop_column('course', 'image_url')
    op.drop_index(op.f('ix_chapter_name'), table_name='chapter')
    op.drop_table('chapter')
    # ### end Alembic commands ###
