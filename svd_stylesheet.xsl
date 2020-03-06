<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!--

Stylesheet for Shearwater SVD schema

-->
<xsl:template match="/device">
<html>
	<head>
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
		<style type="text/css">
			body {
				font-family: "Lato","proxima-nova","Helvetica Neue",Arial,sans-serif;
				font-size: 13px;
			}
			table {
				border: 2px solid #666;
				border-collapse: collapse;
				padding: 0;
				margin: 10px;
				position:relative;
				<!-- border-spacing: 2px 0; -->
			}

			table table {
				border: none;
				margin: 0;
			}

			table th,
			table td {
				border: 1px solid #666;
				vertical-align:top;
			}
			
			table th {
				background-color: #acf;
				padding: 5px;
				position:sticky;
				top:0;
				z-index:10;
				height: 20px;
			}

			table table th {background-color: #aaa; top:30px; z-index:8;}
			table table table th {background-color: #ccc; top:60px; z-index:4;}

			table.leftheader th {text-align:left;}
			table.leftheader th,
			table.leftheader td {
			padding: 5px;
			}
			
			td div {padding: 10px;}
			td td div {padding: 0 10px; font-size: 12px;}
			td th {font-size: 12px;}
				
			tr > td:first-child{
				font-family: monospace;
			}
			
			.togglehidden {
				display:block;
			}
			.togglehidden th {
				position:static;
			}
			a.togglebtn {
				display:block;
				width:100%;
				text-align:center;
				white-space: nowrap;
				padding:5px;
			}


		</style>
	</head>
<body>
<h2>Device:</h2>
<table class="leftheader">
	<xsl:for-each select="*">
		<xsl:if test="name(.) != 'peripherals'">
			<tr><th><xsl:value-of select ="local-name()"/></th><td><xsl:value-of select="." /></td></tr>
		</xsl:if>
	</xsl:for-each>
</table>

<h2>Peripherals:</h2>
<xsl:for-each select="peripherals">
	<xsl:for-each select="peripheral">
	<table class="leftheader">
		<xsl:for-each select="*">
			<xsl:if test="name(.) != 'registers'">
				<tr><th><xsl:value-of select ="local-name()"/></th><td><xsl:value-of select="." /></td></tr>
			</xsl:if>
		</xsl:for-each>
	</table>
	<h3>Registers</h3>
	<table>
		<xsl:for-each select="registers">
			<xsl:for-each select="register">
				<xsl:if test="position()=1">
					<!-- just loop thru first item to get field names for header -->
					<tr>
						<xsl:for-each select="*">
							<th><xsl:value-of select ="local-name()"/></th>
						</xsl:for-each>
					</tr>
				</xsl:if>
				<tr>
					<xsl:for-each select="*">
						<xsl:choose>
							<xsl:when test="name(.) = 'fields'">
								<!-- list each field nicely -->
								<td>
									<table>
										<xsl:for-each select="field">
											<xsl:if test="position()=1">
												<tr bgcolor="#fff">
													<xsl:for-each select="*">
														<th><xsl:value-of select ="local-name()"/></th>
													</xsl:for-each>
												</tr>
											</xsl:if>
											<tr>
												<xsl:for-each select="*">
													<xsl:choose>
														<xsl:when test="name(.) = 'enumeratedValues'">
															<!-- list each value nicely-->
															<td>
															<a href="#" class='togglebtn'>show/hide values</a>
															<table border="2" class="enumeratedValues togglehidden">
																	<xsl:for-each select="enumeratedValue">
																			<xsl:if test="position()=1">
																				<!-- header row -->
																				<thead>
																					<tr bgcolor="#fff">
																						<xsl:for-each select="*">
																							<th><xsl:value-of select ="local-name()"/></th>
																						</xsl:for-each>
																					</tr>
																				</thead>
																			</xsl:if>
																	</xsl:for-each>
																	<tbody>
																		<xsl:for-each select="enumeratedValue">
																				<tr>
																					<xsl:for-each select="*">
																						<td nowrap="1"><div><xsl:value-of select="." /></div></td>
																					</xsl:for-each>
																				</tr>
																		</xsl:for-each>
																	</tbody>
															</table>
															</td>
														</xsl:when>
														<xsl:otherwise>
															<td><div><xsl:value-of select="." /></div></td>
														</xsl:otherwise>
													</xsl:choose>
												</xsl:for-each>
											</tr>
										</xsl:for-each>
									</table>
								</td>
							</xsl:when>
							<xsl:otherwise>
								<td><div><xsl:value-of select="." /></div></td>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:for-each>
				</tr>
			</xsl:for-each>
		</xsl:for-each>

	</table>
	</xsl:for-each>
</xsl:for-each>

</body>
<script>
	$(".togglehidden").hide();
	$(".togglebtn").on("click", function() {
		// show / hide repetitive data
		$(this).next().slideToggle(200);
		return false;
	});
</script>
</html>
</xsl:template>
</xsl:stylesheet>