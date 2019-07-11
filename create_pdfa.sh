#!/bin/sh

# 'gs', '-dQUIET', '-dBATCH', '-dNOPAUSE', '-dCompatibilityLevel=1.6', '-dNumRenderingThreads=4', '-sDEVICE=pdfwrite', '-dAutoRotatePages=/None', '-sColorConversionStrategy=RGB', '-dAutoFilterColorImages=true', '-dAutoFilterGrayImages=true', '-dJPEGQ=95', '-dPDFA=2', '-dPDFACompatibilityPolicy=1', '-sOutputFile=/home/rbrito/tmp/tmp2pt27bs_', '/home/rbrito/tmp/com.github.ocrmypdf.k0hymyks/layers.rendered.pdf', '/home/rbrito/tmp/com.github.ocrmypdf.k0hymyks/pdfa.ps'

ps2pdf -dQUIET -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -dCompatibilityLevel=1.6 -dNumRenderingThreads=4 -dAutoRotatePages=/None -sColorConversionStrategy=RGB -dAutoFilterColorImages=true -dAutoFilterGrayImages=true -dJPEGQ=95 -dPDFA=2 -dPDFACompatibilityPolicy=1 "$1" ~/bin/pdfa.ps
