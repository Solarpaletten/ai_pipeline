#!/usr/bin/env python3
import sys
from storage.redis.connector import get_redis

if get_redis().ping():
    sys.exit(0)
sys.exit(1)
