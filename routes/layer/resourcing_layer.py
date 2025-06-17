from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from . import layer_bp

@layer_bp.route('/resourcing_layer')
def resourcing_layer():
    return render_template('layer/resourcing_layer.html')
