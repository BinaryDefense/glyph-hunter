from flask import Flask, jsonify, request

app = Flask(__name__)

from app import routes

