from flask import Blueprint

main = Blueprint('main', __name__)

# 导入模型
from ..models import Image, KnowledgePoint

from . import routes