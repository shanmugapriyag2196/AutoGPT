from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from . import layer_bp

@layer_bp.route('/hr_layer')
def hr_layer():
    return render_template('layer/hr_layer.html')
