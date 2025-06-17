from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from . import layer_bp

@layer_bp.route('/development_layer')
def development_layer():
    return render_template('layer/development_layer.html')
