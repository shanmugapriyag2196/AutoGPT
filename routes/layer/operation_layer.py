from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from . import layer_bp

@layer_bp.route('/operation_layer')
def operation_layer():
    return render_template('layer/operation_layer.html')
