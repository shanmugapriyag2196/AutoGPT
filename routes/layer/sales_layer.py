from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from . import layer_bp

@layer_bp.route('/sales_layer')
def sales_layer():
    return render_template('layer/sales_layer.html')
