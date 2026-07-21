##########################################################################
#
# Copyright (c) 2026, Brian R Hanke
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import IECore
import Gaffer
import GafferUI
import GafferSceneUI
import imath
import math
import weakref

class GuideGadget( GafferUI.Gadget ) :

	def __init__( self, tool ) :

		GafferUI.Gadget.__init__( self, "GuideGadget" )
		self.__tool = weakref.ref( tool )

	def renderLayer( self, layer, style, reason ) :

		tool = self.__tool()
		if tool is None or not tool["active"].getValue() :
			return

		titleSafeEnabled = tool["titleSafe"].getValue()
		actionSafeEnabled = tool["actionSafe"].getValue()
		ruleOfThirdsEnabled = tool["ruleOfThirds"].getValue()
		centerCrosshairEnabled = tool["centerCrosshair"].getValue()
		if not ( titleSafeEnabled or actionSafeEnabled or ruleOfThirdsEnabled or centerCrosshairEnabled ) :
			return

		resolutionGate = tool.view().resolutionGate()
		if resolutionGate.isEmpty() :
			return

		viewportGadget = self.ancestor( GafferUI.ViewportGadget )
		with GafferUI.ViewportGadget.RasterScope( viewportGadget ) :

			gateSize = imath.V2f( resolutionGate.max() - resolutionGate.min() )
			lineWidth = tool["lineWidth"].getValue()
			lineColor = tool["lineColor"].getValue()
			tickLength = 10.0

			if titleSafeEnabled:
				titleSize = gateSize * imath.V2f( math.sqrt( 0.8 ) )
				titleSize = ( gateSize - titleSize ) / 2
				titleMin = resolutionGate.min() + titleSize
				titleMax = resolutionGate.max() - titleSize

				edges = [
					( imath.V3f( titleMin.x, titleMin.y, 0 ), imath.V3f( titleMax.x, titleMin.y, 0 ) ),
					( imath.V3f( titleMax.x, titleMin.y, 0 ), imath.V3f( titleMax.x, titleMax.y, 0 ) ),
					( imath.V3f( titleMax.x, titleMax.y, 0 ), imath.V3f( titleMin.x, titleMax.y, 0 ) ),
					( imath.V3f( titleMin.x, titleMax.y, 0 ), imath.V3f( titleMin.x, titleMin.y, 0 ) )
				]
				for p1, p2 in edges:
					style.renderLine( IECore.LineSegment3f( p1, p2 ), lineWidth, lineColor )

				# Tick marks
				center = ( titleMin + titleMax ) / 2.0
				ticks = [
					( imath.V3f( center.x, titleMax.y, 0 ), imath.V3f( center.x, titleMax.y - tickLength, 0 ) ),
					( imath.V3f( center.x, titleMin.y, 0 ), imath.V3f( center.x, titleMin.y + tickLength, 0 ) ),
					( imath.V3f( titleMin.x, center.y, 0 ), imath.V3f( titleMin.x + tickLength, center.y, 0 ) ),
					( imath.V3f( titleMax.x, center.y, 0 ), imath.V3f( titleMax.x - tickLength, center.y, 0 ) )
				]
				for p1, p2 in ticks:
					style.renderLine( IECore.LineSegment3f( p1, p2 ), lineWidth, lineColor )

			if actionSafeEnabled :
				actionSize = gateSize * imath.V2f( math.sqrt( 0.9 ) )
				actionSize = ( gateSize - actionSize ) / 2
				actionMin = resolutionGate.min() + actionSize
				actionMax = resolutionGate.max() - actionSize
				edges = [
					( imath.V3f( actionMin.x, actionMin.y, 0 ), imath.V3f( actionMax.x, actionMin.y, 0 ) ),
					( imath.V3f( actionMax.x, actionMin.y, 0 ), imath.V3f( actionMax.x, actionMax.y, 0 ) ),
					( imath.V3f( actionMax.x, actionMax.y, 0 ), imath.V3f( actionMin.x, actionMax.y, 0 ) ),
					( imath.V3f( actionMin.x, actionMax.y, 0 ), imath.V3f( actionMin.x, actionMin.y, 0 ) )
				]
				for p1, p2 in edges :
					style.renderLine( IECore.LineSegment3f( p1, p2 ), lineWidth, lineColor )

				# Tick marks
				center = ( actionMin + actionMax ) / 2.0
				ticks = [
					( imath.V3f( center.x, actionMax.y, 0 ), imath.V3f( center.x, actionMax.y - tickLength, 0 ) ),
					( imath.V3f( center.x, actionMin.y, 0 ), imath.V3f( center.x, actionMin.y + tickLength, 0 ) ),
					( imath.V3f( actionMin.x, center.y, 0 ), imath.V3f( actionMin.x + tickLength, center.y, 0 ) ),
					( imath.V3f( actionMax.x, center.y, 0 ), imath.V3f( actionMax.x - tickLength, center.y, 0 ) )
				]
				for p1, p2 in ticks:
					style.renderLine( IECore.LineSegment3f( p1, p2 ), lineWidth, lineColor )

			if ruleOfThirdsEnabled :
				divNumH = tool["divNumH"].getValue()
				divNumV = tool["divNumV"].getValue()
				divSize = imath.V2f( gateSize / imath.V2f( divNumH, divNumV ) )

				for v in range(1, divNumV) :
					y = resolutionGate.min().y + ( divSize.y * v )
					p1 = imath.V3f( resolutionGate.min().x, y, 0.0 )
					p2 = imath.V3f( resolutionGate.max().x, y, 0.0 )
					style.renderLine( IECore.LineSegment3f( p1, p2 ), lineWidth, lineColor )
				for h in range(1, divNumH) :
					x = resolutionGate.min().x + ( divSize.x * h )
					p1 = imath.V3f( x, resolutionGate.min().y, 0.0 )
					p2 = imath.V3f( x, resolutionGate.max().y, 0.0 )
					style.renderLine( IECore.LineSegment3f( p1, p2 ), lineWidth, lineColor )

			if centerCrosshairEnabled:
				center = ( resolutionGate.min() + resolutionGate.max() ) / 2.0
				crosshairPercentage = 0.02 # Crosshair adapts to aspect ratio.
				halfSize = ( gateSize * crosshairPercentage ) / 2.0

				crosshairLines = [
					(
						imath.V3f( center.x - halfSize.x, center.y, 0.0 ),
						imath.V3f( center.x + halfSize.x, center.y, 0.0 )
					),
					(
						imath.V3f( center.x, center.y - halfSize.y, 0.0 ),
						imath.V3f( center.x, center.y + halfSize.y, 0.0 )
					)
				]

				for p1, p2 in crosshairLines:
					style.renderLine( IECore.LineSegment3f( p1, p2 ), lineWidth, lineColor )

	def layerMask( self ) :

		return self.Layer.Front

	def renderBound( self ) :

		b = imath.Box3f()
		b.makeInfinite()
		return b

class CameraGuides( GafferUI.Tool ) :

	def __init__( self, view, name = "CameraGuides" ) :

		GafferUI.Tool.__init__( self, view, name )

		self["actionSafe"] = Gaffer.BoolPlug( "actionSafe", defaultValue = False )
		self["titleSafe"] = Gaffer.BoolPlug( "titleSafe", defaultValue = False )
		self["ruleOfThirds"] = Gaffer.BoolPlug( "ruleOfThirds", defaultValue = False )
		self["centerCrosshair"] = Gaffer.BoolPlug( "centerCrosshair", defaultValue = False )
		self["divNumH"] = Gaffer.IntPlug( "divNumH", defaultValue = 3 )
		self["divNumV"] = Gaffer.IntPlug( "divNumV", defaultValue = 3 )
		self["lineWidth"] = Gaffer.FloatPlug( "lineWidth", defaultValue = 1.5 )
		self["lineColor"] = Gaffer.Color4fPlug( "lineColor", defaultValue = imath.Color4f( 0.0, 0.25, 0.0, 1.0 ) )

		self.__guideGadget = GuideGadget( self )
		view.viewportGadget().addChild( self.__guideGadget )

IECore.registerRunTimeTyped( CameraGuides, typeName = "GafferUI::CameraGuides" )
GafferUI.Tool.registerTool( "CameraGuides", GafferSceneUI.SceneView, CameraGuides )

Gaffer.Metadata.registerNode(
	CameraGuides,

	"description", "Guide overlays for the currently active camera.",
	"nodeToolbar:bottom:type", "GafferUI.StandardNodeToolbar.bottom",
	"tool:exclusive", False,

	"toolbarLayout:activator:ruleOfThirdsEnabled", lambda plug : plug["ruleOfThirds"].getValue() == True,

	plugs = {

		"actionSafe" : {

			"description" : "Action safe guide.",
			"toolbarLayout:section" : "Bottom",

		},
		"titleSafe" : {

			"description" : "Title safe guide.",
			"toolbarLayout:section" : "Bottom",

		},
		"ruleOfThirds" : {

			"description" : "Rule of thirds guide.",
			"label" : "Rule of Thirds",
			"toolbarLayout:section" : "Bottom",

		},
		"centerCrosshair" : {

			"description" : "Format center.",
			"label" : "Center",
			"toolbarLayout:section" : "Bottom",

		},
		"divNumH" : {

			"description" : "Custom horizontal divisions.",
			"label" : "Horizontal Divisions",
			"toolbarLayout:visibilityActivator" : "ruleOfThirdsEnabled",
			"toolbarLayout:width" : 50,
			"toolbarLayout:section" : "Bottom",

		},
		"divNumV" : {

			"description" : "Custom vertical divisions.",
			"label" : "Vertical Divisions",
			"toolbarLayout:visibilityActivator" : "ruleOfThirdsEnabled",
			"toolbarLayout:width" : 50,
			"toolbarLayout:section" : "Bottom",

		},
		"lineWidth" : {

			"description" : "Line width.",
			"label" : "Width",
			"toolbarLayout:width" : 50,
			"toolbarLayout:section" : "Bottom",

		},
		"lineColor" : {

			"description" : "Guide color.",
			"label" : "Color",
			"toolbarLayout:width" : 200,
			"toolbarLayout:section" : "Bottom",

		},

	},
)
