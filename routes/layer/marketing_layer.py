from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from . import layer_bp

@layer_bp.route('/marketing_layer')
def marketing_layer():
    return render_template('layer/marketing_layer.html')
